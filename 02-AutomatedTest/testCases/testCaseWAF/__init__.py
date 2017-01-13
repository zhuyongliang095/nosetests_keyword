# -*- coding: utf-8 -*-
import unittest
from lib.runRemoteKey import runRemoteKey
from etc.read_conf import waf

def setUp():
    runRemoteKey(waf.client,'set_static_ip',inter=waf.cli_test_inter,ip=waf.cli_test_inter_ip,netmask=24)
    runRemoteKey(waf.server,'set_static_ip',inter=waf.ser_test_inter,ip=waf.ser_test_inter_ip,netmask=24)
    runRemoteKey(waf.server,'http_serv',ip=waf.ser_test_inter_ip,port=80)
    runRemoteKey(waf.server,'http_serv',ip=waf.ser_test_inter_ip,port=8008)
     
def tearDown():
    runRemoteKey(waf.client, 'static_ip_del', inter=waf.cli_test_inter, ip=waf.cli_test_inter_ip, netmask=24)
    runRemoteKey(waf.server,'http_serv_stop' )
    runRemoteKey(waf.server,'static_ip_del', inter=waf.ser_test_inter, ip=waf.ser_test_inter_ip, netmask=24)