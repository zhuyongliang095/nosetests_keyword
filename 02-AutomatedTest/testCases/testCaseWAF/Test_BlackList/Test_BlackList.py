# -*- coding: utf-8 -*-

import unittest
import time
from lib.runRemoteKey import runRemoteKey
from etc.read_conf import waf
from etc.read_conf import web_status_code

class test_blackip(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        runRemoteKey(waf.client, 'waf_api',url='http://'+waf.waf_ge1_ip+':8080/api/blackip/'+waf.cli_test_inter_ip,action='DELETE',expect=None)
    
    def test_blockip_add_del_run(self):
        print('ok=',web_status_code.ok)
        print('type(ok)=',type(web_status_code.ok))
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip',
                     action='POST', RequestPayload={'ip': waf.cli_test_inter_ip}, expect_status=web_status_code.ok
                     )
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip',
                     action='GET', expectPayload={'ip': waf.cli_test_inter_ip}, expect_status=web_status_code.ok
                     )
        runRemoteKey(waf.client, 'http_cli', url='http://'+waf.waf_ge1_ip,
                     expect=1,status_code=web_status_code.forbidden
                     )
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip/'+waf.cli_test_inter_ip,
                     action='DELETE', expect_status=web_status_code.ok
                     )
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip',
                     action='GET', expect=0, expectPayload={'ip': waf.cli_test_inter_ip}
                     )
        runRemoteKey(waf.client, 'http_cli',url='http://'+waf.waf_ge1_ip, expect=1 )

    def test_add_error_blockip(self):
        runRemoteKey(waf.client, 'waf_api',url='http://'+waf.waf_ge1_ip+':8080/api/blackip',
                     action='POST', RequestPayload={'ip': '1.1.1.256'}, expect_status=web_status_code.unprocessableentity,
                     )
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip',
                     action='GET', expect=0, expectPayload={'ip': '1.1.1.256'},
                     )
        
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip',
                     action='POST', RequestPayload={'ip': '0.1.1.2'}, expect_status=web_status_code.unprocessableentity
                     )
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip',
                     action='GET', expect=0, expectPayload={'ip': '0.1.1.2'},
                     )
        
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip',
                     action='POST', RequestPayload={'ip': '255.255.255.255'}, expect_status=web_status_code.unprocessableentity
                     )
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip',
                     action='GET',expect=0, expectPayload={'ip': '255.255.255.255'}
                     )
        
    def test_del_no_exist(self):
        runRemoteKey(waf.client, 'waf_api', url='http://'+waf.waf_ge1_ip+':8080/api/blackip/200.100.20.1',
                     action='DELETE', expect_status=web_status_code.notfound
                     )
    
    
if __name__ == '__main__':
    unittest.main()