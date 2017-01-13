# -*- coding: utf-8 -*-

from classes.tapfighter import TapFighter
from pymongo import MongoClient
from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

@app.route('/fighter', methods=['GET'])
def search():
    return search_by_name(request.args.get('name').replace('%20',' '))

@app.route('/fighter', methods=['POST'])
def create():
    pass


def search_by_name(name, second_time=False):
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
    if cursor.count() > 0:
        temp_list = []
        for document in cursor:
            document.pop('_id')
            temp_list.append(document)
        return jsonify(temp_list)
    elif second_time == False:
        # 数据库里找不到就去Tapology搜索
        tapfighters = TapFighter(name)

        if tapfighters.fighters:
            for each_found_fighter in tapfighters.fighters:
                result = fighters.insert_one(json.loads(each_found_fighter.to_json()))

            return search_by_name(name, True)
        else:
            return -1
    else:
        return -1



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