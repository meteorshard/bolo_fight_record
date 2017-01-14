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

    URL Args: 
        name: 待查找的名字，可以有空格
        target: 从哪里查找，可用选项为local/remote

    Returns:
        [
            {
    
            },
            {
    
            },
            ...
        ]

    """
    name = request.args.get('name')
    if name:
        if request.args.get('target') == 'local':

            # 连接数据库
            bfr_client = MongoClient()
            db = bfr_client.bolofightrecord

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
                fighters_found_list = []
                for document in cursor:
                    # 把无法序列化的字段干掉
                    document.pop('_id')
                    fighters_found_list.append(document)
                return jsonify(fighters_found_list)

        elif request.args.get('target') == 'remote':
            return 'No target', 404
        else:
            return 'No name', 404

    else:
        return 'Nothing found', 404
    # return search_by_name(request.args.get('name').replace('%20',' '))








if __name__ == '__main__':
    bfr_app.run(debug=True)