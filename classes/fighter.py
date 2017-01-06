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
            self.__searchFighterAtTapology(stringToSearch)
        

    '''-----搜索选手-----'''
    def __searchFighterAtTapology(self, fighterName): 
        s = requests.session()
        nameToSearch = fighterName.replace(' ','+')                                         # 把空格用加号代替方便搜索
        url = u'http://www.tapology.com/search'
        payload = {'term': nameToSearch}
        header = {
                'Accept-Encoding':'gzip, deflate',
                'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                'Host':"www.tapology.com",
                'Referer':"http://www.tapology.com/",
                'X-Requested-With':"XMLHttpRequest"
        }
        searchResult = s.get(url, params=payload, headers=header)

        soup = BeautifulSoup(searchResult.content, "html.parser")

        pattern = re.compile(r'/fightcenter/fighters/.*')                                   # 匹配搜索结果的正则表达式

        for link in soup.find_all('a', href=pattern):
            fighterPageUrl = u'http://www.tapology.com' + link.get('href')
            break #只找第一个

        if fighterPageUrl:
            fighterResult = self.__analyzeFighterDetailPage(fighterPageUrl)                 # 解析详情页面
        else:
            print(u'Didn\'t find anything.')
            return

    '''-----解析详情页-----'''
    def __analyzeFighterDetailPage(self, url):
        if url[:8] == u'testpage':                                                          # 如果载入的是测试用本地页面
            detailPageSoup = BeautifulSoup(open(url,encoding='utf-8'), 'html.parser')
        else:
            s = requests.session()
            header = {
                'Accept-Encoding':'gzip, deflate',
                'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                'Host':"www.tapology.com",
                'Referer':"http://www.tapology.com/",
                'X-Requested-With':"XMLHttpRequest"
            }
            cookies = {
                '_tapology_session_3_2':'VEpoMERtRCtWMkNQaWtmMWxydjZnZGY0bXFPSXV2RW5qWU5NYkRjaGNwd3RxOHRDZ0RVczBOSUF6RFRlQy9yMStmdlhpbUdRZUlVdEtBeTVjMURNd0VGMW1GbFdwMlJOTDdVa3BoNXMyQ3NZM3Z2TG5SaDN4OE1aWnJEMEczZlNJLytBTVM5MUx6RW5FUDRJUVZEbElEdFovSEFTdXA3aHM3NVJaYlNOa2IwVzZOd1hBaW1HTmhXN0pyK2NZbnlkLS1hVVM2bzB1RnVqQlN1ZmVibGNJSnN3PT0%3D--9357e61cae9d1d39244a1e628a76a1ac62561a96',
                'remember_id':'99440',
                'remember_token':'a398d9b35578002069660e5994a47775229c77a04b8f6c90aa0af51fbcb8b479',
                '__utma':'268593006.152914935.1462258111.1466749671.1466839275.27',
                '__utmb':'268593006.5.10.1466839275',
                '__utmc':'268593006',
                '__utmv':'268593006.|1=logged_in=yes=1',
                '__utmz':'268593006.1463202945.10.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)'
            }
            detailPage = s.get(url, headers=header, cookies = cookies)
            detailPageSoup = BeautifulSoup(detailPage.content, 'html.parser')

        detailSector = detailPageSoup.find('div', class_='details')                         # 解析个人资料详情区域----------------------------

        eachLi = detailSector.find_all('li')

        fighterDetail = {}                                                                  # 初始化一个dict来存储详细信息

        for li in eachLi:                                                                   # 取每个单元格的内容
            strongItems = li.find_all('strong')                                             # 粗体的是类别，比如名字、绰号什么的
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
                        else:                                                               # 如果没下一项内容了就跳出循环，继续找<strong>
                            break
                        thisTag = nextTag                                                   # thisTag指向下一项，继续循环

                    fighterDetail[eachStrongItem.get_text().lstrip('| ').rstrip(':')] = detailThisStrong

        recordSector = detailPageSoup.find_all('table', class_='fightRecord')               # 解析战绩----------------------------
        fightRecordAll = []
        for recordRow in recordSector[0].tbody.tr.find_all('tr'):                           # 每行对应一条比赛纪录，循环获取——这里有bug，Tapology页面里少写了一个/tr
            thisRecord = {}
            recordCols = recordRow.find_all('td')

            if len(recordCols) >= 4:                                                        # 只有四列的才可能是战绩
                resultSpans = recordCols[0].find_all('span')                                # 第一列：比赛结果。有两种格式，一种里面有span（新的），一种没有
                if resultSpans:                                                             # 有span，新格式
                    thisRecord['Result'] = resultSpans[0].get_text(strip=True)              # 第一个span肯定是结果的文本描述
                    if len(resultSpans) >= 2:                                               # 如果有两个或者以上的span，说明有比赛时间信息
                        thisRecord['Time'] = resultSpans[1].get_text(strip=True)
                else:                                                                       # 没span是旧格式
                    thisRecord['Result'] = recordCols[0].get_text(strip=True)               

                opponentA = recordCols[1].find_all('a')                                     # 第二列：对手
                thisOpponent = {}                                                           # 搞个dict来存储对手信息，两个keyword分别是名字和页面地址
                if opponentA:
                    thisOpponent['Name'] = opponentA[0].get_text().encode('utf-8')          # 名字里有奇怪的葡语字符要编码成utf-8
                    thisOpponent['Url'] = opponentA[0].get('href')
                thisRecord['Opponent'] = thisOpponent

                fightRecordAll.append(thisRecord)


        if ('Name' in fighterDetail.keys()):
            self.name = fighterDetail['Name'][0]
        elif('Given Name' in fighterDetail.keys()):
            self.name = fighterDetail['Given Name'][0]

        if ('Nickname' in fighterDetail.keys()):    
            self.aka = fighterDetail['Nickname'][0]

        if ('Affiliation' in fighterDetail.keys()):    
            self.affiliation = fighterDetail['Affiliation'][0]

        if ('Height' in fighterDetail.keys()): 
            self.height = re.search(r'\([1-2]\d{2}cm\)',fighterDetail['Height'][0]).group(0).lstrip('(').rstrip('cm)')

        if ('Reach' in fighterDetail.keys()): 
            self.reach = re.search(r'\([1-2]\d{2}cm\)',fighterDetail['Reach'][0]).group(0).lstrip('(').rstrip('cm)')

        if ('Date of Birth' in fighterDetail.keys()):
            yearBirth, monthBirth, dayBirth = fighterDetail['Date of Birth'][0].split('.')
            self.birthday = datetime(int(yearBirth),int(monthBirth),int(dayBirth))

        if fightRecordAll:
            self.fightRecord = fightRecordAll






        