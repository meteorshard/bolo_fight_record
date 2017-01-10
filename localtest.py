# -*- coding: utf-8 -*-

from classes.fighter import Fighter
from pymongo import MongoClient
from flask import Flask, request
import re

app = Flask(__name__)

@app.route('/')
def index():
    return process(request.args.get('fighter').replace('%20',' '))

def process(name):
    bolofightrecord_client = MongoClient()
    db = bolofightrecord_client.bolofightrecord
    fighters = db.fighters

    name_regex = ''
    name_splited = name.split(' ')
    print(name_splited)
    for each_word in name_splited:
        name_regex = name_regex + r'\b' + each_word + '.*'
        print(name_regex)
    name_regex = r'.*\b' + name_regex
    print(name_regex)
    cursor = fighters.find({'name':re.compile(name_regex,re.IGNORECASE)})
    if cursor.count() > 0:
        print('Found!')
        for fighterfound in cursor:
            # print(repr(fighterfound))
            return fighterfound['name']
    else:
        return 'Not found'


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