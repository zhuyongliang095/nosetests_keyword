# -*- coding: utf-8 -*-

import unittest
import time
from lib.runRemoteKey import runRemoteKey
from etc.read_conf import waf
from etc.read_conf import web_status_code

def setUp():
    print(" test_whitelist setup")
    
def tearDown():
    print(" test_whitelist teardown")


class test_whilelist(unittest.TestCase):
    def setUp(self):
        print(" test_whilelist class setup ")
    
    def tearDown(self):
        print(" test_whilelist class teardown ")
    
    def test_whilelist_add_run_del(self):
        print("test whilelist case")

if __name__ == '__main__':
    unittest.main()