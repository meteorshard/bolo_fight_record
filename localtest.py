# -*- coding: utf-8 -*-

from classes.fighter import Fighter
from pymongo import MongoClient
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/fighter', methods=['GET'])
def search():
    return search_by_name(request.args.get('name').replace('%20',' '))

@app.route('/fighter', methods=['POST'])
def create():
    pass


def search_by_name(name):
    # 连接数据库
    bolofightrecord_client = MongoClient()
    db = bolofightrecord_client.bolofightrecord
    fighters = db.fighters

    # 分词和构建正则表达式
    name_regex = ''
    name_splited = name.split(' ')
    for each_word in name_splited:
        name_regex = name_regex + r'\b' + each_word + r'.*'
    name_regex = r'.*\b' + name_regex
    # 按照正则表达式进行搜索，忽略大小写
    cursor = fighters.find({'name': re.compile(name_regex, re.IGNORECASE)})
    # 如果有查找结果
    fighters_return = []
    if cursor.count() > 0:
        print('Found!')
        for fighter_found in cursor:
            if ('fightrecord' in fighter_found.keys()):
                for each_fight_record in fighter_found['fightrecord']:
                    if ('Name' in each_fight_record['Opponent'].keys()):
                        each_fight_record['Opponent']['Name'] = each_fight_record['Opponent']['Name'].decode()
                fighter_dict = {
                    'name': fighter_found['name'],
                    'aka': fighter_found['aka'],
                    'fightrecord': fighter_found['fightrecord'],
                }
            fighters_return.append(fighter_dict)      
        # return repr(fighters_return)
    else:
        # 数据库里找不到就去Tapology搜索
        tapfighter = Fighter(name)

        fighter_detail = {
            'name': tapfighter.name,
            'aka': tapfighter.aka,
            'fightrecord': tapfighter.fightrecord
        }

        result = fighters.insert_one(fighter_detail)

        fighter_detail.pop('_id', None)

        for each_fight_record in fighter_detail['fightrecord']:
            if 'Opponent' in each_fight_record.keys():
                if 'Name' in each_fight_record['Opponent'].keys():
                    each_fight_record['Opponent']['Name'] = each_fight_record['Opponent']['Name'].decode()

        fighters_return.append(fighter_detail)
        # print(repr(fighters_return))

    return jsonify({'fighter': fighters_return})

# def tt_localtest():
#     test_fighter = Fighter('sdfaksdlfasd')
#     print(test_fighter.name)
#     print(test_fighter.aka)
#     print(test_fighter.weightclass)
#     # print(repr(test_fighter.fightrecord))

#     tt_client = MongoClient()
#     db = tt_client.bolofightrecord
#     fighters = db.fighters

#     cursor = fighters.find({'name':test_fighter.name})

#     if cursor.count() > 0:
#         print('Found!')
#         for fighterfound in cursor:
#             print(repr(fighterfound))
#     else:
#         print('Not found! Insert new record...')
#         result = fighters.insert_one(
#             {
#                 'name': test_fighter.name,
#                 'aka': test_fighter.aka,
#                 'fightrecord':test_fighter.fightrecord
#             }
#         )
#         if result:
#             print('Done.')


if __name__ == '__main__':
    app.run(debug=True)