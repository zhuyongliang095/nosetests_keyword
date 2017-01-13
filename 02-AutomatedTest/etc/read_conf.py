# -*- coding:utf-8 -*-  

import configparser2
import sys,os
from lib.public import local_system 
from lib.public import ExpectError

class getconfig(object):
    def __init__(self,section):
        self.getconfig(section)
    
    def __getfilePath(self,config):
        if "Linux" in local_system:
            return os.path.split(os.path.realpath(__file__))[0]+'/'+config
        elif "Windows" in local_system:
            return os.path.split(os.path.realpath(__file__))[0]+'\\'+config
    
    def __getSMCHost(self):
        conf_path=self.__getfilePath('config.conf')
        #print("conf_path {}".format(conf_path))
        cf=configparser2.ConfigParser()
        cf.readfp(open(conf_path))
        section='SMC'
        options=cf.options(section)
        for option in options:
            setattr(self,option,cf.get(section,option))
            
    def getconfig(self,section):
        conf_path=self.__getfilePath('config.conf')
        cf=configparser2.ConfigParser()
        cf.readfp(open(conf_path))
        try:
            options=cf.options(section)
            for option in options:
                setattr(self,option,cf.get(section,option))
        except :
            raise ExpectError('no section {}'.format(section))
    
    
smc=getconfig('SMC')
waf=getconfig('WAF')
web_status_code=getconfig('WEBSTATUSCODE')

if __name__ == '__main__':
    #pdb.set_trace()
    smc=getconfig('SMC')
    print("dut: {}".format(smc.controller))
    waf=getconfig('WAF')
    print("dut1: {}".format(waf.waf))
    print("dut1_passwd: {}".format(waf.waf_passwd))
    web_status_code=getconfig('WEBSTATUSCODE')
    print('web_status_code : {}'.format(web_status_code.ok))