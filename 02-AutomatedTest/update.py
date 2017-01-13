# -*- coding:utf-8 -*-  
import os,subprocess,threading,socket
from configure import svn_path
class update(object):
    path='C:\\Python27\\Lib\\site-packages\\AutomatedLib'
    thr=None

    def __init__(self):
        pass

    def svn_up(self):
        if os.path.isdir(self.path)  :
            cmd="svn update " + self.path
            print("svn update %s"% self.path)
            svn_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
            svn_pipe.wait()
            if svn_pipe.returncode==0 :
                print("svn update success")
                return True
            else:
                print("svn update failed")
                return False
            svn_pipe.kill()
        else:
            cmd="svn chechout " + svn_path + "  "+ self.path
            svn_pipe=subprocess.Popen(cmd,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE,shell=True)
            svn_pipe.wait()
            if svn_pipe.returncode==0 :
                print("svn checkout success, path:%s"%self.path) 
                return True
            else:
                print("svn checkout failed, path:%s"%self.path)
                return False
            svn_pipe.kill()
    def stop_local_Rserver(self):
        from robot.libraries.Remote import Remote
        local_server=Remote(uri="http://127.0.0.1:8270")
        local_server.run_keyword(name="stop_remote_server",args="",kwargs="")
        print("local server is stop")

    def start_local_Rserver(self):
        cmd="python "+self.path+"\\Remotelibrary.py"
        #self.thr=threading.Thread(target=subprocess.Popen,args=(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True))
        self.thr=threading.Thread(target=subprocess.Popen,args=(cmd,))
        self.thr.setDaemon=True
        self.thr.start()
        print("local server is start")

    def monitor(self):
        HOST='0.0.0.0'
        PORT=11211
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        print("update port is start, ip:%s,port:%s"%(HOST,str(PORT)))
        self.start_local_Rserver()
        while 1:
            message, address = s.recvfrom(8192)
            if message == "update" :
                self.stop_local_Rserver()
                
                if self.svn_up() == True:
                    message="update success"
                else :
                    message="svn update failed"
                self.start_local_Rserver()
                s.sendto(message,address)
            else:
                message="no command"
                print("unknow command,failed")
                sendto(message,adddress)


if __name__ == "__main__" :
    test=update()
    test.monitor()