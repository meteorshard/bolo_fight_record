# -*- coding: utf-8 -*-

from classes.tapfighter import TapFighter
from pprint import pprint

def main():
    tapfighter_test = TapFighter('conor mcgregor')

    for each_fighter in tapfighter_test.fighters:
        print(each_fighter.to_json())

if __name__ == '__main__':
    main()