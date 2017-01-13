# -*- coding:utf-8 -*-  
import socket
import multiprocessing
import sys
import time
from lib.publib import _char2uni,_searchchar,ExpectError

class socket_transmission():
    tcp_s={}
    udp_s={}
    def __init__(self):
        pass
    
    def _tcp_server(self,ip=None,port=1000,ip_type=4):
        if int(ip_type) == 4:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            s=socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((ip,port))
        except socket.error,err_msg:
            raise ExpectError(message="Bind local %s:%d failed(%s)."%(ip,port,err_msg))
        else:
            s.listen(10)
            s.settimeout(None)
            while True:
                conn,addr=s.accept()
                print("Connected by %s"%str(addr))
                data=conn.recv(8192)
                print("%s recv data:\"%s\" from %s"%(str(s.getsockname()),data,str(addr)))
                conn.sendall('Done')
            conn.close()

    def tcp_server(self,ip=None,port=1000,ip_type=4):
        """
        Listen local IP and port
        """
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        ip=_char2uni(ip)
        port=int(_char2uni(port))
        ip_type=_char2uni(ip_type)
        if int(ip_type) != 4 or int(ip_type) !=6 :
            p=multiprocessing.Process(target=self._tcp_server,args=(ip,port,ip_type,))
        else:
            raise ExpectError("ip_type error")
        p.start()
        self.tcp_s[port]=p

    def tcp_server_stop(self,port=1000):
        """
        port = None, kill all listen port.
        port = num, kill the num port for listen.
        """
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        port=int(_char2uni(port))
        if port == None or str(port) == 'None' :
            for port in self.tcp_s:
                self.tcp_s[port].terminate()
                self.tcp_s[port].join()
        else :
            try :
                port=int(port)
            except ValueError,msg:
                raise ExpectError(message="\"port\" is not a number.\(%s\)"%msg)
            else:
                try:
                    self.tcp_s[int(port)].terminate()
                    self.tcp_s[int(port)].join()
                except KeyError,msg:
                    raise ExpectError(message="\"port is error. \(%s\)\""%msg)
    
    def tcp_client(self,ip=None,port=1000,ip_type=4,expect=1):
        """"
        expect = 1 is success
        expect = 0 is fail
        """
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        ip=_char2uni(ip)
        port=int(_char2uni(port))
        ip_type=_char2uni(ip_type)
        expect=_char2uni(expect)
        stat=0
        if int(ip_type) == 4 :
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif int(ip_type) == 6:
            s=socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            raise ExpectError("ip_type error")
        try:
            s.settimeout(1.0)
            s.connect((ip,port))
        except (socket.error,socket.timeout) as e:
            if int(expect)==0 :
                print("Expect connect Failed, actually Failed")
            else:
                raise ExpectError(message="Connect Server %s:%d is failed(%s)."%(ip,port,e))
        else:
            send_data='send one world!'
            s.sendall(send_data)
            recv_data=s.recv(8192)
            print("%s recv data:\"%s\" from %s "%(str(s.getsockname()),recv_data,str(s.getpeername())))
        finally:
            s.close()
        if int(expect) == 0:
            raise ExpectError(message="Expect Failed,actually Success!")
        
    def _udp_server(self,ip=None,port=1000,ip_type=4):
        if int(ip_type) == 4 :
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else :
            s=socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try :
            s.bind((ip,port))
            s.setblocking(1)
        except socket.error,err_msg:
            raise ExpectError(message="Bind local %s:%d failed(%s)."%(ip,port,err_msg))
        else:
            while True:
                message,address=s.recvfrom(8192)
                print("%s:%d recv data:\"%s\" from %s"%(ip,port,message,str(address)))
                if int(ip_type) == 4:
                    s.sendto("Done",address)
                else:
                    s.sendto("Done",(address[0],address[1]))
    
    def udp_server(self,ip=None,port=1000,ip_type=4):
        """
        Listen local IP and port
        """
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        ip=_char2uni(ip)
        port=int(_char2uni(port))
        ip_type=_char2uni(ip_type)
        if int(ip_type) == 4 or int(ip_type) == 6 :
            p=multiprocessing.Process(target=self._udp_server,args=(ip,port,ip_type,))
        else:
            raise ExpectError("ip_type error!")
        #p=multiprocessing.Process(target=self._udp_server,args=(ip,port,ip_type,))
        p.daemon=True
        p.start()
        self.udp_s[port]=p
    
    def udp_server_stop(self,port=1000):
        """
        port = None, kill all listen port.
        port = num, kill the num port for listen.
        """
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        port=_char2uni(port)
        if port == None or str(port) == 'None' :
            for port in self.udp_s:
                self.udp_s[port].terminate()
                self.udp_s[port].join()
        else :
            try :
                port=int(port)
            except ValueError ,msg :
                raise ExpectError(message="\"port\" is not a number.\(%s\)"%msg)
            else:
                try:
                    self.udp_s[int(port)].terminate()
                    self.udp_s[int(port)].join()
                except KeyError,msg:
                    raise ExpectError(message="\"port is error. \(%s\)\""%msg)
    
    def udp_client(self,ip=None,port=1000,ip_type=4,expect=1):
        """"
        expect = 1 is success
        expect = 0 is fail
        """
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        ip=_char2uni(ip)
        port=int(_char2uni(port))
        ip_type=_char2uni(ip_type)
        expect=_char2uni(expect)
        stat=1
        if int(ip_type) == 4 or ip_type == None :
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif int(ip_type) == 6 :
            s=socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        else:
            raise ExpectError("ip_type error!")
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        addr=(ip,port)
        s_msg='Send one udp packet!'
        try:
            s.connect(addr)
            s.settimeout(1.0)
            for i in range(2):
                s.sendall(s_msg)
                print("%s  Send  data:\"%s\" to %s"%(s.getsockname(),s_msg,str(addr)))
                r_msg=s.recv(2048)
                if not len(r_msg):
                    print("%s recv no data  from %s"%(str(s.getsockname()),str(addr)))
                else:
                    print("%s recv data:\"%s\" from %s"%(str(s.getsockname()),r_msg,str(addr)))
        except (socket.error,socket.timeout) as msg:
            print("socket:%s"%msg)
            stat=0
        finally:
            s.close()
        if int(expect) == int(stat):
            print("Expect is %s, actually is %s"%("Success" if int(expect) == 1 else "failed","success" if int(stat) == 1 else "failed"))
        else:
            raise ExpectError(message="Expect is %s, actually is %s"%("Success" if int(expect) == 1 else "failed","success" if int(stat) == 1 else "failed"))
        
if __name__ == '__main__':
    ip='172.16.1.100'
    s=socket_transmission()
    s.tcp_server(ip=ip,port=2000)
    s.tcp_client(ip=ip,port=2000)
    s.tcp_client(ip=ip,port=2000)
    s.tcp_client(ip=ip,port=2000)
    s.tcp_server_stop(None)
    s.udp_server(ip=ip)
    time.sleep(20)
    s.udp_client(ip=ip)
    s.udp_server_stop()