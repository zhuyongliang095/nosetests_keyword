#-*- coding: utf-8 -*-
'''
Created on 2017年1月8日

@author: zhuyongliang
'''

import re
import chardet
import platform

def __working_host_system():
    if platform.system() == 'Linux' :
        return {'Linux':None}
    elif platform.system() == 'Windows' :
        if re.search('2003',platform.release()) or re.search('xp',platform.release()) :
            return {'Windows':6}
        elif re.search('7',platform.release()) or re.search('10',platform.release()) :
            return {'Windows':7}
    else :
        raise ExpectError("no support OS")
    
local_system=__working_host_system()


def ip_change(startip='',count=None):
    ip=[startip]
    ip_old=startip.split('.')
    for i in range(count-1):
        ip_old[3]=int(ip_old[3])+1
        if int(ip_old[3]) == 255 :
            ip_old[3]=1
            ip_old[2]=int(ip_old[2])+1
            if int(ip_old[2]) == 255 :
                ip_old[2] = 1
                ip_old[1] = int(ip_old[1])+1
                if int(ip_old[1])==255:
                    ip_old[1] = 1
                    ip_old[0] = int(ip_old[0])+1
        for a in range(len(ip_old)):
            ip_old[a]=str(ip_old[a])
        ip.append('.'.join(ip_old))
    return ip

class ExpectError(Exception):
    """Custom expected error for automated test"""
    def __init__(self, message=None):
        self.message=message
    def __str__(self):
        return("%s"%self.message)
    
def _searchchar(searchc,chars,expect,tpye='cmd'):
    if tpye=='cmd' :
        reobj=re.compile('%|Error')
        if expect == None or str(expect) == 'None' or expect == '':
            print("disinterest result!")
        elif reobj.search(chars)  :
            if int(expect) != 0:
                raise ExpectError(message="expect run command success ,actually run failed")
            else :
                print("expect run command failed,actually run failed")
        else:
            if int(expect) == 0:
                raise ExpectError(message="expect run command failed ,actually run success")
            else:
                print("expect run command success,actually run success")

    if searchc != None and str(searchc) != str('None') and searchc != '':
        reobj=re.compile(searchc,re.M)
        if expect == None or str(expect) == 'None' :
            return reobj.search(chars)
        else:
            if reobj.search(chars) :
                if int(expect) == 1:
                    print("search %s : except success,actually success"%searchc)
                    return_char=reobj.findall(chars)
                    while (type(return_char) != str and type(return_char) != unicode ):
                        return_char=return_char[0]
                    return return_char
                else:
                    print('The Search String :', chars)
                    print('Search for the String :', searchc)
                    raise ExpectError("search %s : except fail,actually success"%searchc)
            else:
                if int(expect) == 1:
                    print('The Search String :', chars)
                    print('Search for the String :', searchc)
                    raise ExpectError("search %s : except success,actually failed"%searchc)
                else:
                    print("search %s : except fail,actually fail"%searchc)

def _char2uni(strings):
    if strings == b'' :
        return ''
    if isinstance(strings, str):
        return unicode(strings,chardet.detect(strings)['encoding'])
    elif isinstance(strings,list) or isinstance(strings,tuple):
        dicts=[]
        for i in range(len(strings)) :
            if strings[i] != b'' :
                dicts.append(unicode(strings[i],chardet.detect(strings[i])['encoding']))
        return dicts