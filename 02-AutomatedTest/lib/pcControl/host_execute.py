# coding=utf-8

import subprocess
import time
import sys
from lib.public import _searchchar
from lib.public import ExpectError
from lib.public import _char2uni

class host_execute_cmd():
    def __init__(self):
        pass
    
    def host_execute_cmd(self,cmd='',searchchar=None, expect=1, timeout=None,*args,**kwargs):
        '''execute cmd in Host
        cmd=ls
        searchchar='root'
        expect=1，have and 0 is not have,None or 'None'
        timeout,wait time for execute cmd.
        '''
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,kwargs))
        print("{:<20} : {:<30}".format('cmd',cmd))
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        if timeout != None and timeout != 'None' :
            t=0
            while t <= timeout:
                time.sleep(1)
                p.poll()
                if p.returncode == 0 :
                    break
                t+=1
            p.poll()
            if p.returncode == None :
                p.terminate()
                if expect == 1 :
                    raise ExpectError('Execute {cmd} timeout !!'.format(cmd))
                elif expect == 0 :
                    print("execut cmd : {} timeout,expect error.".format(cmd))
                elif expect == None or expect == "None" :
                    pass
        msgs=p.communicate()
        msgs='\n'.join(_char2uni(msgs))
        print(msgs)
        return _searchchar(searchchar,msgs,expect=expect,tpye='pc')

if __name__ == '__main__' :
    execute=host_execute_cmd()
    execute.host_execute_cmd('ping 172.17.0.1 -n 1', None, 1, timeout=1)