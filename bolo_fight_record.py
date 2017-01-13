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
    if request.args.get('name'):
        if request.args.get('target') == 'local':
            pass
        elif request.args.get('target') == 'remote':
            pass

    else:
        return '404', 404
    # return search_by_name(request.args.get('name').replace('%20',' '))








if __name__ == '__main__':
    bfr_app.run(debug=True)