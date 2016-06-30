'''
Created on 30 Jun 2016

@author: martin
'''

def one():
    return None


def two(condition):
    if condition:
        print('here')
    elif condition is None:
        print('nor')
    else:
        print('there')

