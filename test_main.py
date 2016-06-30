'''
Created on 30 Jun 2016

@author: martin
'''
import unittest
import tested

class Test(unittest.TestCase):


    def test_first(self):
        self.assertEqual(tested.one(), None)
        
    def test_other(self):
        tested.two(False)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_first']
    unittest.main()