# -*- coding: utf-8 -*-

from classes.tapfighter import TapFighter

from pymongo import MongoClient
from flask import Flask, request, jsonify

import json
import re

bfr_app = Flask(__name__)

@bfr_app.route('/api/v0.1/fighter', methods=['GET'])
def search():
    """ 查找选手资料
    如果选项是local就在本地数据库查找
    如果是remote则去tapology.com查找，并写入/更新本地数据库
    无论是哪种渠道，只要查找到结果，就以JSON格式返回

    请求格式：

        Example:
        /api/v0.1/fighter?name=conor mcgregor&target=local

    URL Args: 
        name: 待查找的名字，可以有空格
        target: 从哪里查找，可用选项为local/remote

    Returns:
        [
          {
            "affiliation": "10th Planet Jiu Jitsu", 
            "aka": "Hurricane", 
            "birthday": "1979.02.11", 
            "fight_records": [
              {
                "result": "Loss | KO/TKO | Punches", 
                "time": "2:52 Round 3 of 3, 12:52 Total"
              }, 
              {
                "result": "Win | Decision | Unanimous", 
                "time": "3 Rounds, 15:00 Total"
              }
            ], 
            "height": "178", 
            "name": "Conor Heun", 
            "personal_pages": [
              "http://www.twitter.com/ConorHeun"
            ], 
            "reach": "183", 
            "weight": "155.0", 
            "weight_class": "Lightweight"
          }, 
          {
            "affiliation": "Straight Blast Gym Ireland", 
            "aka": "The Notorious", 
            "birthday": "1988.07.14", 
            "fight_records": [
              {
                "result": "Win | KO/TKO | Punches", 
                "time": "3:04 Round 2 of 5, 8:04 Total"
              }, 
              {
                "result": "Win | Decision | Majority", 
                "time": "5 Rounds, 25:00 Total"
              }
            ], 
            "height": "175", 
            "name": "Conor McGregor", 
            "personal_pages": [
              "http://www.twitter.com/TheNotoriousMMA", 
              "http://www.facebook.com/thenotoriousmma"
            ], 
            "reach": "188", 
            "weight": "154.4", 
            "weight_class": "Lightweight"
          }
        ]

    """
    name = request.args.get('name')
    target = request.args.get('target')

    if name and target:
        # 连接数据库
        URI = 'mongodb://root:pgM9px0RO1syxXR0FMOqAHZC4mvmIuNFyDCAezEY@jcaferaanzdw.mongodb.sae.sina.com.cn:10453,snxggenumogl.mongodb.sae.sina.com.cn:10453'
        bfr_client = MongoClient(URI)
        db = bfr_client.bolofightrecord

        fighters_found_list = []

        # 如果请求的是查找本地数据库
        if target == 'local':
             # 分词和构建正则表达式
            name_regex = ''
            name_splited = name.split(' ')
            for each_word in name_splited:
                name_regex = name_regex + r'\b' + each_word + r'.*'
            name_regex = r'.*\b' + name_regex

            # 按照正则表达式进行搜索，忽略大小写
            cursor = db.fighters.find({'name': re.compile(name_regex, re.IGNORECASE)})

            # 如果有查找结果
            if cursor.count() > 0:
                for document in cursor:
                    # 把无法序列化的字段干掉
                    document.pop('_id')
                    fighters_found_list.append(document)
            else:
                return 'Nothing found', 404

        # 如果请求查找的是远程数据（Tapology上的）
        elif request.args.get('target') == 'remote':
            tapfighters = TapFighter(name)

            if tapfighters.fighters:
                for each_fighter_found in tapfighters.fighters:
                    fighters_found_list.append(each_fighter_found.serialize())
                    result = db.fighters.insert_one(each_fighter_found.serialize())
        else:
            return 'Wrong target', 404

        return jsonify(fighters_found_list)

    else:
        return 'No name', 404


if __name__ == '__main__':
    bfr_app.run(debug=True)