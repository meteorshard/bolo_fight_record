# -*- coding: utf-8 -*-

from classes.tapfighter import TapFighter

def main():
    tapfighter_test = TapFighter('holly holm')

    print(tapfighter_test.name)
    print(tapfighter_test.aka)

if __name__ == '__main__':
    main()