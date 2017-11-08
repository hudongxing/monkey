# -*- coding: utf-8 -*-
__author__ = "violet"
# @Time  : 2017/9/8 10:36
# @Author: 胡东兴

import os


class AndroidDebugBridge:
    def call_adb(self, command):
        command_result = ''
        command_text = 'adb %s' % command
        results = os.popen(command_text, "r")
        while 1:
            line = results.readline()
            if not line:
                break
            command_result += line
        results.close()
        command_result = command_result.split("	")[0]
        return command_result

        # 检查设备

    def attached_devices(self):
        result = self.call_adb("devices")
        devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
        return [device for device in devices if len(device) > 2]

    # check for any fastboot device
    def fastboot(self, device_id):
        pass


if __name__ == '__main__':
    reuslt = AndroidDebugBridge().attached_devices()
    for info in reuslt:
        print(info)
