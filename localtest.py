# -*- coding: utf-8 -*-

from classes.fighter import Fighter

def tt_localtest():
    test_fighter = Fighter('Ronda Rousey')
    print(test_fighter.name)
    print(test_fighter.aka)
    print(test_fighter.weightclass)

if __name__ == '__main__':
    tt_localtest()