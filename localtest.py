# -*- coding: utf-8 -*-

from classes.tapfighter import TapFighter


if __name__ == '__main__':
    taptest = TapFighter('Conor')
    print(repr(taptest.fighters[0].serialize()))