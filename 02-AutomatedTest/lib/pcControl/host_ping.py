#coding=utf-8

import sys
import subprocess
import re
from lib.public import _char2uni
from lib.public import ExpectError
from lib.public import local_system
class ping(object):
    def __init__(self):
        pass
    
    def host_ping(self,inter='test',hostip=None,num=2,times=2,expect=1,**kwargs):
        '''inter : NIC name,
        hostip : target IP  of ping
        times : 超时次数
        expect : 1代表成功，0代表失败，None or 'None' 代表不关心结果
        
        '''
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,kwargs))
        msgs=[]
        stat=0
        for i in range(int(times)) :
            tmp_msgs=[]
            if 'Linux' in local_system:
                cmd='ping '+str(hostip)+' -c '+str(num)
            elif "Windows" in local_system :
                cmd='ping '+str(hostip)+' -n '+str(num)
            print("%s"%cmd)
            p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
            p.wait()
            read_stdout=p.stdout.read()
            read_stderr=p.stderr.read()
            if 'Windows' in local_system :
                p.terminate()
            if read_stdout != None and read_stdout != b'' :
                tmp_msgs.extend(_char2uni(read_stdout).split('\r\n'))
            #print('read_stderr {}'.format(read_stderr))
            if read_stderr != None and read_stderr != b'' :
                tmp_msgs.extend(_char2uni(read_stderr).split('\r\n'))
            msgs.extend(tmp_msgs)
            reobj=re.compile(u'\(0% loss\)|\(0% 丢失\)|0% packet loss')
            tmp_msgs=' '.join(tmp_msgs)
            if reobj.search(tmp_msgs) :
                stat = 1
                break
        print('\n'.join(msgs))
        if expect != 'None' and expect != None :
            if int(stat) == int(expect) :
                print("Expect is %s, actually %s"%('success' if int(expect) == 1 else 'fail','success' if int(expect) == 1 else 'fail'))
            else:
                raise ExpectError(message="Expect is %s, actually %s"%("Success" if int(expect) == 1 else "failed","success" if int(stat) == 1 else "failed"))
            
if __name__ == '__main__':
    pc=ping()
    pc.host_ping(inter='test',hostip='172.17.0.1',num=1,times=3,expect=1)
    pc.host_ping(inter='test',hostip='172.17.20.1',num=1,times=3,expect=None)
