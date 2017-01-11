# -*- coding: utf-8 -*-

from classes.tapfighter import TapFighter

def main():
    tapfighter_test = TapFighter('mike')

    for each_fighter in tapfighter_test.fighters:
        print(each_fighter.name)
        print(each_fighter.aka)

if __name__ == '__main__':
    main()