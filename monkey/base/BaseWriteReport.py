# -*- coding: utf-8 -*-
__author__ = "violet"
# @Time  : 2017/9/8 16:29
# @Author: 胡东兴

import os
import xlsxwriter
from base import BaseReport

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def report(info):
    workbook = xlsxwriter.Workbook('report.xlsx')
    bo = BaseReport.OperateReport(workbook)
    bo.monitor(info)
    bo.analysis(info)
    bo.crash()
    bo.close()

