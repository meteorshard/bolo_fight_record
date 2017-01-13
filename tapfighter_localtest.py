# -*- coding: utf-8 -*-

from classes.tapfighter import TapFighter

def main():
    tapfighter_test = TapFighter('ronda')

    for each_fighter in tapfighter_test.fighters:
        print(each_fighter.to_json())

if __name__ == '__main__':
    main()