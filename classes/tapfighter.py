# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

class TapFighter(object):
    ''' 数据来自Tapology.com的选手类

    Attributes:
        fighters: 具体选手Fighter类的实例 list

    '''

    class Fighter(object):
        ''' 选手详情类

        Attributes:
            name: 选手名字 string
            aka: 绰号 string
            affliation: 战队 string
            height: 身高 float
            weight: 体重 float
            reach: 臂展 float
            weight_class: 重量级 string
            fight_records: 战绩 list
                Example:
                [ 
                    { 
                        "Time" : "2:52 Round 3 of 3, 12:52 Total", 
                        "Result" : "Loss | KO/TKO | Punches", 
                        "Opponent" : { 
                            "Name" : BinData(0,"UnlhbiBDb3V0dXJl"), 
                            "Url" : "/fightcenter/fighters/ryan-couture" 
                        } 
                    }, 
                    { 
                        "Time" : "3 Rounds, 15:00 Total", 
                        "Result" : "Win | Decision | Unanimous", 
                        "Opponent" : { 
                            "Name" : BinData(0,"TWFnbm8gQWxtZWlkYQ=="), 
                            "Url" : "/fightcenter/fighters/magno-almeida" 
                        } 
                    } 
                ]
        '''

        def __init__(self):
            ''' 构造函数
            
            给选手类赋初值

            '''

            self.name = ''
            self.aka = ''
            self.affliation = ''
            self.height = 0
            self.weight = 0
            self.reach = 0
            self.weight_class = ''
            self.birthday = datetime(1799, 1, 1)
            self.fight_records = []


    def __init__(self, text_to_search):
        ''' 构造函数

        1. 初始化选手属性
        2. 传入搜索参数并调用对应函数进行搜索

        Args:
            text_to_search: 用于在tapology.com上搜索的字符串，可以是选手姓名或者网页

        '''

        self.fighters = []

        # 判断参数到底是不是网页
        if (text_to_search[:7]=='http://') or (text_to_search[-4:]=='html'):
            # 如果一看就是网页url
            self.__analyze_detail_page(text_to_search)
        else:
            # 否则当做选手名字处理
            # 先获取详情页地址
            fighter_urls = self.__search(text_to_search)
            # 如果有，就再解析详情页
            if fighter_urls:
                for url in fighter_urls:
                    self.fighters.append(self.__analyze_detail_page(url))

                    if len(self.fighters) >= 3:
                        break

    def __search(self, fighter_name):
        ''' 搜索选手名字，解析搜索结果页，获取详情页地址

        Args: 
            fighter_name: 选手名字

        Returns:
            返回详情页url列表

        '''
        s = requests.session()

        # 把空格用加号代替方便搜索
        name_to_search = fighter_name.replace(' ','+')
        url = u'http://www.tapology.com/search'
        payload = {'term': name_to_search}
        header = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Connection':'keep-alive',
                'Host':'www.tapology.com',
                'Referer':'http://www.tapology.com/',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36Accept-Encoding:gzip, deflate, sdch'
        }
        cookies = {
            '_tapology_session_3_2':'dlg2SHI5Qk16dWk3enZDYUNaWExtT2F5L3FyV21TY2ZrTXZBcHM2N0tkRTdUanhUcldZdW9kRDJGUGJuNU1WYnU0VWRQcitwbDd5MHdlcHdpYk9wNEVkYW1ZQVZRZEx3YjJRSHNHWnlvTlVxcFI4WFpHN0FWK2Iyb2IzQW5hVWRqRHN1WHkzeFRIR05pMjdkcTYydGdReHd2ZitWdjBlN2VPeWV5N2tHdVBDMldBQ3lXdjR5ZzVBdU83emllZ1ZHLS1XV1RrWWN5czQ5cGZSbWNFRlA0UStnPT0%3D--9ae26d9d0925a8c6a041bd5b74f79516c818db59'
        }
        search_result = s.get(url, params=payload, headers=header, cookies=cookies)
        soup = BeautifulSoup(search_result.content, "html.parser")

        # 匹配选手详情页url的正则表达式
        pattern = re.compile(r'/fightcenter/fighters/.*')

        # 解析搜索结果
        detail_page_urls = []
        for link in soup.find_all('a', href=pattern):
            detail_page_urls.append(u'http://www.tapology.com' + link.get('href'))

        # 返回搜索到的详情页list
        return detail_page_urls

    def __analyze_detail_page(self, url):
        ''' 解析详情页

        Args:
            url: 传入的详情页url

        Returns:
            返回Fighter类

        '''
        s = requests.session()
        header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Host':'www.tapology.com',
            'Referer':'http://www.tapology.com/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36Accept-Encoding:gzip, deflate, sdch'
        }
        cookies = {
            '_tapology_session_3_2':'dlg2SHI5Qk16dWk3enZDYUNaWExtT2F5L3FyV21TY2ZrTXZBcHM2N0tkRTdUanhUcldZdW9kRDJGUGJuNU1WYnU0VWRQcitwbDd5MHdlcHdpYk9wNEVkYW1ZQVZRZEx3YjJRSHNHWnlvTlVxcFI4WFpHN0FWK2Iyb2IzQW5hVWRqRHN1WHkzeFRIR05pMjdkcTYydGdReHd2ZitWdjBlN2VPeWV5N2tHdVBDMldBQ3lXdjR5ZzVBdU83emllZ1ZHLS1XV1RrWWN5czQ5cGZSbWNFRlA0UStnPT0%3D--9ae26d9d0925a8c6a041bd5b74f79516c818db59'
        }
        detail_page = s.get(url, headers=header, cookies=cookies)
        soup = BeautifulSoup(detail_page.content, 'html.parser')

        # 解析个人资料详情区域
        detail_sector = soup.find('div', class_='details')
        each_li = detail_sector.find_all('li')

        # 建一个空的Fighter对象
        fighter = self.Fighter()
        # 用来临时存储选手详细数据（除了战绩）
        temp_detail = {}

        ''' 取每个单元格的内容
            粗体的是类别,比如名字、绰号什么的
            Example:

            <li class="noPadStripe">
                <strong>Name:</strong>
                <span>Mike Adams</span>
            </li>
            <li class="Stripe">
                <strong>MMA Record:</strong>
                <span>7-4-0 (Win-Loss-Draw)</span>
            </li>
        '''
        for li in each_li:
            strong_items = li.find_all('strong')

            if strong_items:
                for each_strong_item in strong_items:
                    # 用个列表来存储可能的多项内容
                    detail_this_strong = []
                    # this_tag指向第一个内容
                    this_tag = each_strong_item.next_sibling.next_sibling

                    # 如果内容存在（至少一项）则判断是文字还是链接
                    if this_tag:                                                             
                        if this_tag.name == 'a':
                            detail_this_strong.append(this_tag.get('href'))
                        elif this_tag.name == 'span':
                            detail_this_strong.append(this_tag.get_text())

                        # 如果还存在下一项内容
                        if this_tag.next_sibling.next_sibling:
                            # next_tag指向下一项内容
                            next_tag = this_tag.next_sibling.next_sibling

                            # 判断是文字还是链接
                            if next_tag.name == this_tag.name:                                    
                                if next_tag.name == 'a':
                                    detail_this_strong.append(next_tag.get('href'))
                                elif next_tag.name == 'span':
                                    detail_this_strong.append(next_tag.get_text())
                            else:
                                # 如果没下一项内容了就跳出循环,继续找<strong>
                                break
                            # this_tag指向下一项,继续循环
                            this_tag = next_tag                                                   

                    # 先丢到临时存储里面去，稍后循环结束了再整理
                    temp_detail[each_strong_item.get_text().lstrip('| ').rstrip(':')] = detail_this_strong

        # 把临时存储整理到Fighter对象去
        # 选手姓名
        if 'Name' in temp_detail:
            fighter.name = temp_detail['Name'][0]
        elif 'Given Name' in temp_detail:
            fighter.name = temp_detail['Given Name'][0]

        # 选手绰号
        if 'Nickname' in temp_detail:
            if temp_detail['Nickname'][0] != r'N/A':
                fighter.aka = temp_detail['Nickname'][0]

        # 选手组织
        if 'Affiliation' in temp_detail:    
            fighter.affiliation = temp_detail['Affiliation'][0]

        # 选手重量级
        if 'Weight Class' in temp_detail: 
            fighter.weight_class = temp_detail['Weight Class'][0]

        # 选手身高
        if 'Height' in temp_detail: 
            fighter.height = re.search(r'\([1-2]\d{2}cm\)',temp_detail['Height'][0]).group(0).lstrip('(').rstrip('cm)')

        # 选手臂展
        if 'Reach' in temp_detail: 
            fighter.reach = re.search(r'\([1-2]\d{2}cm\)',temp_detail['Reach'][0]).group(0).lstrip('(').rstrip('cm)')

        # 选手生日
        if 'Date of Birth' in temp_detail:
            yearBirth, monthBirth, dayBirth = temp_detail['Date of Birth'][0].split('.')
            fighter.birthday = datetime(int(yearBirth),int(monthBirth),int(dayBirth))

        ''' 下面开始解析战绩部分
        战绩区域是一个class_='fightRecord'的table
        每个<tr>是一行，但并不是每行都是战绩
        如果一行有超过4个<td>说明这一行是具体的战绩

        Example:

        <tr>
            <td class="result">
                <span class="hoverTool" title="Bout Page">
                    <a href="/fightcenter/bouts/285016-ufc-fight-night-103-yair-el-pantera-rodriguez-vs-bj-the-prodigy-penn">Confirmed Upcoming Bout</a>
                </span>
            </td>
            <td>
                <p class="fightRecordOverflow">
                    <span>
                        <img class="fightRecordFlag" src="/assets/flags/MX-d65aa1408646b5deb96ccac71e5198c6.gif" alt="Mx">
                        <a href="/fightcenter/fighters/70995-yair-rodriguez">Yair Rodriguez</a>
                    </span>
                    <br>
                    <span class="left">16-10-2</span>
                    <span class="right">9-1-0</span>
                </p>
            </td>
            <td>
                <p class="fightRecordOverflow">
                    <img class="fightRecordFlag" src="/assets/flags/US-5781b16534d0a403efbc7d336f1667b8.gif" alt="Us">
                    <a href="/fightcenter/events/42582-ufc-fight-night">UFC Fight Night 103: Rodriguez vs. Penn</a>
                    <br>
                    <span>Main Event | Featherweight | 145 lbs</span>
                </p>
            </td>
            <td class="date">2017.01.15</td>
        </tr>
        
        '''

        # 获取战绩区域
        record_sector = soup.find_all('table', class_='fightRecord')

        # 获取战绩区域的所有行
        for each_record_row in record_sector[0].tbody.tr.find_all('tr'):
            record_cols = each_record_row.find_all('td')
            # 如果一行超过4个<td>说明这是要找的战绩行
            if len(record_cols) >= 4:


        return fighter


