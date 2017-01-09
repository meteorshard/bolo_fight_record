# -*- coding: utf-8 -*-

from classes.fighter import Fighter

def tt_localtest():
    conor = Fighter('Conor McGregor')
    print(conor.name)
    print(conor.aka)

if __name__ == '__main__':
    tt_localtest()