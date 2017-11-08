# -*- coding: utf-8 -*-
__author__ = "violet"
# @Time  : 2017/9/8 10:20
# @Author: 胡东兴
import os
import time
import shutil
import subprocess
from base import AdbCommon
from multiprocessing import Pool
from base import BasePhoneMsg
from base.BaseFile import OperateFile
from base.BasePickle import writeFlowInfo, writeInfo, writeSum, readInfo
from base import BaseMonkeyConfig
import uuid
import datetime
from base import BaseMonitor
from base.BaseWriteReport import report

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
ba = AdbCommon.AndroidDebugBridge()


def killport():
    os.system(PATH('./kill5037.bat'))
    os.popen("adb kill-server adb")
    os.popen("adb start-server")


def runnerPool():
    # if os.path.exists((PATH("./info/"))):
    #     shutil.rmtree((PATH("./info/")))  # 删除持久化目录
    #     os.makedirs(PATH("./info/"))  # 创建持久化目录
    # else:
    #     os.makedirs(PATH("./info/"))  # 创建持久化目录
    devices_Pool = []
    devices = ba.attached_devices()
    if devices:
        for item in range(0, len(devices)):
            _app = {"devices": devices[item], "num": len(devices)}
            devices_Pool.append(_app)
        start(devices_Pool[0])
    else:
        print("设备不存在")


def start(devicess):
    makedir()
    devices = devicess["devices"]
    num = devicess["num"]
    app = {}
    mkdirInit(devices, app, num)
    mc = BaseMonkeyConfig.monkeyConfig(PATH("monkey.ini"))
    mc["log"] = PATH("./log") + "\\" + str(uuid.uuid4())
    mc["monkey_log"] = mc["log"] + "monkey.log"
    mc["cmd"] = mc['cmd'] + mc["monkey_log"]
    # print(mc)
    # print(type(mc))
    start_monkey("adb -s " + devices + " shell " + mc["cmd"], mc["log"])
    time.sleep(1)
    starttime = datetime.datetime.now()
    pid = BaseMonitor.get_pid(mc["package_name"], devices)
    cpu_kel = BaseMonitor.get_cpu_kel(devices)
    beforeBattery = BaseMonitor.get_battery(devices)
    # print(pid, cpu_kel, beforeBattery)
    while True:
        with open(mc["monkey_log"], encoding='utf-8') as monkeylog:
            time.sleep(1)  # 每1秒采集检查一次
            BaseMonitor.cpu_rate(pid, cpu_kel, devices)
            BaseMonitor.get_men(mc["package_name"], devices)
            BaseMonitor.get_fps(mc["package_name"], devices)
            BaseMonitor.get_flow(pid, mc["net"], devices)
            BaseMonitor.get_battery(devices)
            if monkeylog.read().count('Monkey finished') > 0:
                endtime = datetime.datetime.now()
                print(str(devices) + "测试完成咯")
                writeSum(1, path=PATH("./info/sumInfo.pickle"))
                app[devices]["header"]["beforeBattery"] = beforeBattery
                app[devices]["header"]["afterBattery"] = BaseMonitor.get_battery(devices)
                app[devices]["header"]["net"] = mc["net"]
                app[devices]["header"]["monkey_log"] = mc["monkey_log"]
                app[devices]["header"]["time"] = str((endtime - starttime).seconds) + "秒"
                writeInfo(app, PATH("./info/info.pickle"))
                break
                # go.info[devices]["header"]["sumTime"] = str((endtime - starttime).seconds) + "秒"
                # report(go.info)
    if readInfo(PATH("./info/sumInfo.pickle")) <= 0:

        report(readInfo(PATH("./info/info.pickle")))
        subprocess.Popen("taskkill /f /t /im adb.exe", shell=True)
        shutil.rmtree((PATH("./info/")), ignore_errors=False, onerror=None) # 删除持久化目录
        # cmd2 = "adb logcat -d >%s" % PATH("./log") + "\\" + r"11111111111111111111logcat.log"
        # os.popen(cmd2)
        print("------来吧------")
# 开始脚本测试
def start_monkey(cmd, log):
    # Monkey测试结果日志:monkey_log
    # mc = BaseMonkeyConfig.monkeyConfig(PATH("monkey.ini"))
    # os.popen(mc["closedsys"])
    os.popen(cmd)
    print('==========================================')
    print(cmd)
    print("==========================================")
    # Monkey时手机日志,logcat
    logcatname = PATH("./log") + "\\" + str("logcat.log")
    cmd2 = "adb logcat  >%s" % logcatname
    os.popen(cmd2)
    # "导出traces文件"
    tracesname = log + r"traces.log"
    cmd3 = "adb shell cat /data/anr/traces.txt>%s" % tracesname
    os.popen(cmd3)


def mkdirInit(devices, app, data=None):
    # destroy(devices)
    cpu = PATH("./info/" + devices + "_cpu.pickle")
    men = PATH("./info/" + devices + "_men.pickle")
    flow = PATH("./info/" + devices + "_flow.pickle")
    battery = PATH("./info/" + devices + "_battery.pickle")
    fps = PATH("./info/" + devices + "_fps.pickle")
    app[devices] = {"cpu": cpu, "men": men, "flow": flow, "battery": battery, "fps": fps, "header": get_phone(devices)}
    OperateFile(cpu).mkdir_file()
    OperateFile(men).mkdir_file()
    OperateFile(flow).mkdir_file()
    OperateFile(battery).mkdir_file()
    OperateFile(fps).mkdir_file()
    OperateFile(PATH("./info/sumInfo.pickle")).mkdir_file()  # 用于记录是否已经测试完毕，里面存的是一个整数
    OperateFile(PATH("./info/info.pickle")).mkdir_file()  # 用于记录统计结果的信息，是[{}]的形式
    writeSum(0, data, PATH("./info/sumInfo.pickle"))  # 初始化记录当前真实连接的设备数


def get_phone(devices):
    bg = BasePhoneMsg.get_phone_Kernel(devices)
    app = {"phone_name": bg[0]["phone_name"] + "_" + bg[0]["phone_model"] + "_" + bg[0]["release"], "pix": bg[3],
           "rom": bg[1], "kel": bg[2]}
    return app

def makedir():

    if os.path.exists(PATH("./info/")):
        pass
    else:
        os.makedirs(PATH("./info"))


if __name__ == '__main__':
    killport()
    time.sleep(1)
    runnerPool()
    # makedir()