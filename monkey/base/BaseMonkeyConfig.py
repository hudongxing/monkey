# -*- coding: utf-8 -*-
__author__ = "violet"
# @Time  : 2017/9/8 14:44
# @Author: 胡东兴

import configparser
import time
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def monkeyConfig(init_file):
    config = configparser.ConfigParser()
    config.read(init_file)
    app = {"package_name": config['DEFAULT']['package_name'], "net": config['DEFAULT']['net'],
           "cmd": config['DEFAULT']['cmd'] + ">", "closedsys": config['DEFAULT']['closedsys']}
    # app["activity"] = config['DEFAULT']['activity']
    return app
