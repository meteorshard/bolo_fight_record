# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

'''-----选手类-----'''
class Fighter(object):
    def __init__(self, stringToSearch):
        super(Fighter, self).__init__()
        
        if (stringToSearch[:7]=='http://') or (stringToSearch[-4:]=='html'):                # 如果传进来的是url就直接解析页面
            self.__analyzeFighterDetailPage(stringToSearch)
        else:                                                                               # 否则就去搜索名字
            self.__analyzeFighterDetailPage(self.__searchFighterAtTapology(stringToSearch))
        

    '''-----搜索选手-----'''
    def __searchFighterAtTapology(self, fighterName): 
        s = requests.session()
        nameToSearch = fighterName.replace(' ','+')                                         # 把空格用加号代替方便搜索
        url = u'http://www.tapology.com/search'
        payload = {'term': nameToSearch}
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
        searchResult = s.get(url, params=payload, headers=header, cookies=cookies)

        soup = BeautifulSoup(searchResult.content, "html.parser")

        pattern = re.compile(r'/fightcenter/fighters/.*')                                   # 匹配搜索结果的正则表达式

        
        # 搜索结果
        fighterPageUrl = None
        for link in soup.find_all('a', href=pattern):
            fighterPageUrl = u'http://www.tapology.com' + link.get('href')
            break #只找第一个

        # 如果结果不为空
        if fighterPageUrl is not None:
            return fighterPageUrl                 # 解析详情页面
        else:
            print(u'Err: Didn\'t find anything.')
            return -1

    '''-----解析详情页-----'''
    def __analyzeFighterDetailPage(self, url):
        if url != -1:
            if url[:8] == u'testpage':                                                          # 如果载入的是测试用本地页面
                detailPageSoup = BeautifulSoup(open(url,encoding='utf-8'), 'html.parser')
            else:
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
                detailPage = s.get(url, headers=header, cookies=cookies)
                detailPageSoup = BeautifulSoup(detailPage.content, 'html.parser')
        else:
            print(u'Nothing to analyze.')
            return -1

        detailSector = detailPageSoup.find('div', class_='details')                         # 解析个人资料详情区域----------------------------

        eachLi = detailSector.find_all('li')

        fighterDetail = {}                                                                  # 初始化一个dict来存储详细信息

        for li in eachLi:                                                                   # 取每个单元格的内容
            strongItems = li.find_all('strong')                                             # 粗体的是类别,比如名字、绰号什么的
            if strongItems:
                for eachStrongItem in strongItems:
                    detailThisStrong = []                                                   # 用个列表来存储可能的多项内容
                    thisTag = eachStrongItem.next_sibling.next_sibling                      # thisTag指向第一个内容
                    if thisTag:                                                             # 如果内容存在（至少一项）则判断是文字还是链接
                        if thisTag.name == 'a':
                            detailThisStrong.append(thisTag.get('href'))
                        elif thisTag.name == 'span':
                            detailThisStrong.append(thisTag.get_text())

                    while thisTag.next_sibling.next_sibling:                                # 如果还存在下一项内容
                        nextTag = thisTag.next_sibling.next_sibling                         # nextTag指向下一项内容
                        if nextTag.name == thisTag.name:                                    # 判断是文字还是链接
                            if nextTag.name == 'a':
                                detailThisStrong.append(nextTag.get('href'))
                            elif nextTag.name == 'span':
                                detailThisStrong.append(nextTag.get_text())
                        else:                                                               # 如果没下一项内容了就跳出循环,继续找<strong>
                            break
                        thisTag = nextTag                                                   # thisTag指向下一项,继续循环

                    fighterDetail[eachStrongItem.get_text().lstrip('| ').rstrip(':')] = detailThisStrong

        recordSector = detailPageSoup.find_all('table', class_='fightRecord')               # 解析战绩----------------------------
        fightRecordAll = []
        for recordRow in recordSector[0].tbody.tr.find_all('tr'):                           # 每行对应一条比赛纪录,循环获取——这里有bug,Tapology页面里少写了一个/tr
            thisRecord = {}
            recordCols = recordRow.find_all('td')

            if len(recordCols) >= 4:                                                        # 只有四列的才可能是战绩
                resultSpans = recordCols[0].find_all('span')                                # 第一列：比赛结果。有两种格式,一种里面有span（新的）,一种没有
                if resultSpans:                                                             # 有span,新格式
                    thisRecord['Result'] = resultSpans[0].get_text(strip=True)              # 第一个span肯定是结果的文本描述
                    if len(resultSpans) >= 2:                                               # 如果有两个或者以上的span,说明有比赛时间信息
                        thisRecord['Time'] = resultSpans[1].get_text(strip=True)
                else:                                                                       # 没span是旧格式
                    thisRecord['Result'] = recordCols[0].get_text(strip=True)               

                opponentA = recordCols[1].find_all('a')                                     # 第二列：对手
                thisOpponent = {}                                                           # 搞个dict来存储对手信息,两个keyword分别是名字和页面地址
                if opponentA:
                    thisOpponent['Name'] = opponentA[0].get_text().encode('utf-8')          # 名字里有奇怪的葡语字符要编码成utf-8
                    thisOpponent['Url'] = opponentA[0].get('href')
                thisRecord['Opponent'] = thisOpponent

                fightRecordAll.append(thisRecord)


        # 选手姓名
        if ('Name' in fighterDetail.keys()):
            self.name = fighterDetail['Name'][0]
        elif('Given Name' in fighterDetail.keys()):
            self.name = fighterDetail['Given Name'][0]
        else:
            self.name = ''

        # 选手绰号
        if ('Nickname' in fighterDetail.keys()):    
            self.aka = fighterDetail['Nickname'][0]
        else:
            self.aka = ''

        # 选手组织
        if ('Affiliation' in fighterDetail.keys()):    
            self.affiliation = fighterDetail['Affiliation'][0]
        else:
            self.affiliation = ''

        # 选手重量级
        if ('Weight Class' in fighterDetail.keys()): 
            self.weightclass = fighterDetail['Weight Class'][0]
        else:
            self.weightclass = ''


        # 选手身高
        if ('Height' in fighterDetail.keys()): 
            self.height = re.search(r'\([1-2]\d{2}cm\)',fighterDetail['Height'][0]).group(0).lstrip('(').rstrip('cm)')
        else:
            self.height = ''

        # 选手臂展
        if ('Reach' in fighterDetail.keys()): 
            self.reach = re.search(r'\([1-2]\d{2}cm\)',fighterDetail['Reach'][0]).group(0).lstrip('(').rstrip('cm)')
        else:
            self.reach = ''

        # 选手生日
        if ('Date of Birth' in fighterDetail.keys()):
            yearBirth, monthBirth, dayBirth = fighterDetail['Date of Birth'][0].split('.')
            self.birthday = datetime(int(yearBirth),int(monthBirth),int(dayBirth))
        else:
            self.birthday = ''

        # 选手战绩
        ''' 示例
        [
            {
                'Time': '0:48 Round 1 of 5', 
                'Result': 'Loss | KO/TKO | Punches', 
                'Opponent': {
                    'Url': '/fightcenter/fighters/amanda-nunes-lioness-of-the-ring', 
                    'Name': b'Amanda Nunes'
                }
            }, 
            {
                'Result': 'Cancelled Bout', 
                'Opponent': {
                    'Url': '/fightcenter/fighters/18698-holly-holm-hottie', 
                    'Name': b'Holly Holm'
                }
            }
        ]
        '''
        if fightRecordAll:
            self.fightrecord = fightRecordAll
        else:
            self.fightrecord = ''






        