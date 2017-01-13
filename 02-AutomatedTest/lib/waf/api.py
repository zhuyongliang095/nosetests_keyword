# -*- coding: utf-8 -*-

import requests
import json
import pdb
import sys
import time

from lib.public import ExpectError 
from lib.public import _searchchar
from lib.public import _char2uni

class api(object):
    def __init__(self):
        pass
    
    def __GetAction(self,action):
        try :
            return getattr(requests,action)
        except :
            raise
    
    def __ToStrings(self,Dict):
        try:
            return json.dumps(Dict)
        except :
            print(u"{Dict} is not dics.  type is {types} ".format(Dict=Dict,types=type(Dict)))
            raise
            
    def __ToDict(self,String):
        try:
            return json.loads(String)
        except:
            print(u"{String} is not str, type is {types}. ".format(String=String,types=type(String)))
            raise
    
    def waf_api(self,url,action="GET",expect=1,*args,**kwargs):
        '''
        action : PUT，DELETE，HEAD 以及 OPTIONS。
        RequestPayload : Client上传的数据。
        expectPayload : Server发送的数据。
        expect_status_code : API请求返回的状态码，默认200。 
        expect : 1 success or 0 fail,expectpayload内容不为空才有效。
        '''
        print("run keyword : {}  {}".format(sys._getframe().f_code.co_name,locals()))
        req=self.__GetAction(action.lower())
        try:
            if 'RequestPayload' in kwargs:
                r=req(url,kwargs['RequestPayload'])
            else :
                r=req(url)
            replayPayloadText=r.text
            time.sleep(5)
            
            if  expect == 1 :
                if 'expectPayload' in kwargs :
                    if 'application/json' in r.headers['Content-Type'] :
                        replyPayload=self.__ToDict(replayPayloadText)
                        if isinstance(kwargs['expectPayload'],str):
                            kwargs['expectPayload']=self.__ToDict(kwargs['expectPayload'])
                        if kwargs['expectPayload']  not in replyPayload['data'] :
                            raise ExpectError('expectPayload eroor : expect %s, actually %s'%(kwargs['expectPayload'],replayPayloadText))
                    #elif 'text' in r.headers['Content-Type'] :
                    else :
                        print("headers :",r.headers)
                        raise ExpectError('use wrong keyword.')
                    
                if 'expect_status_code' in kwargs and int(kwargs['expect_status_code']) != r.status_code :
                    raise ExpectError('status_code eroor : expect %s, actually %s'%(kwargs['expect_status_code'], r.status_code ))
                
            elif expect == 0 :
                if 'expectPayload' in kwargs :
                    if 'json'in r.headers['Content-Type'] :
                        replyPayload=self.__ToDict(replayPayloadText)
                        if isinstance(kwargs['expectPayload'],str):
                            kwargs['expectPayload']=self.__ToDict(kwargs['expectPayload'])
                        if kwargs['expectPayload']  in replyPayload['data'] :
                            raise ExpectError('expectPayload eroor : expect %s, actually %s'%(kwargs['expectPayload'],replayPayloadText))
                    #elif 'text' in r.headers['Content-Type'] :
                    else :
                        raise ExpectError('use wrong keyword.')
                                    
                if 'expect_status_code' in kwargs and int(kwargs['expect_status_code']) == r.status_code :
                    raise ExpectError('status_code eroor : expect %s, actually %s'%(kwargs['expect_status_code'], r.status_code ))
            elif expect == None :
                print("expect is None.")
                
        except :
            if expect == None :
                pass
            else :
                raise 
            
if __name__ == '__main__':
    a=api()
    a.waf_api(url='http://172.17.21.110:8080/api/blackip',action='GET',RequestPayload={'sort':'','page':'1','per_page':'10'},expect_status_code=200)
    a.waf_api(url='http://172.17.21.110:8080/api/blackip/1.1.1.1',action='DELETE',expect=1)
    a.waf_api(url='http://172.17.21.110:8080/api/blackip',action='POST',RequestPayload={"ip":"1.1.1.1"},expect_status_code=200)
    a.waf_api(url='http://172.17.21.110:8080/api/blackip',action='GET',expectPayload={"ip":"1.1.1.1"},expect_status_code=200)
    a.waf_api(url='http://172.17.21.110:8080/api/blackip/1.1.1.1',action='DELETE',expect_status_code=200)
    a.waf_api(url='http://172.17.21.110',action='GET',expectPayload='body',expect_status_code=200)