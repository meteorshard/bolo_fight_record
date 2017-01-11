# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

class TapFighter(object):
    ''' 数据来自Tapology.com的选手类

    Attributes:
        name: 选手名字 string
        aka: 绰号 string
        affliation: 战队 string
        height: 身高 float
        weight: 体重 float
        reach: 臂展 float
        weight_class: 重量级 string
        fight_record: 战绩 list

    '''

    def __init__(self, text_to_search):
        ''' 构造函数

        1. 初始化选手属性
        2. 传入搜索参数并调用对应函数进行搜索

        Args:
            text_to_search: 用于在tapology.com上搜索的字符串，可以是选手姓名或者网页

        '''

        self.name = ''
        self.aka = ''
        self.affliation = ''
        self.height = 0
        self.reach = 0
        self.weight_class = ''
        self.fight_record = []

        # 判断参数到底是不是网页
        if (text_to_search[:7]=='http://') or (text_to_search[-4:]=='html'):
            # 如果一看就是网页url：
            pass
        else:
            # 否则当做选手名字处理：
            pass
