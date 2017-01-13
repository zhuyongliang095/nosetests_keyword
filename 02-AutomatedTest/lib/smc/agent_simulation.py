'''
Created on 2017年1月8日

@author: zhuyongliang
'''
import time
import struct
import socket
import select
from  multiprocessing import process,Queue
import random
import pdb

class agent_simulation(object):
    '''
    simulation agent send pack, this is a Independent process.
    '''
    def __init__(self,localip,targethost,targetport=9070):
        '''
        Constructor
        '''
        self.que=Queue()
        self.localip=localip
        self.targetip=targethost
        self.targetport=targetport
    
    def set_status(self,status,*args,**kwargs):
        '''
        start,stop,restart,showlicense,pause
        if showlicense, add kwargs time=10 , wait show liecense time 10s.
        if pause , add kwargs  time=10, pause time 10s.
        '''
        if status == 'start':
            self.pro=self.__agent_start()
            
        elif status == 'stop':
            self.pro.terminate()
            
        elif status == 'restart':
            self.pro.terminate()
            self.pro=self.__agent_start()
            
        elif status == 'showlicense' :
            self.que.put({status:kwargs})
            agent_license=self.que.get(block=True,timeout=int(kwargs['time'])+5)
            print('agent simulation licnese :\n {}'.format(agent_license))
            
        elif status == 'pause':
            self.que.put({status:kwargs})
            
        print('agent simulation pid : {}'.format(self.pro.pid))
            
    def __sendPackSock(self,local_ip,dstip,port):
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((local_ip,0))
        sock.setblocking(0)
        sock.connect((dstip,port))
        return sock
    
    def __agent_simulation(self,que,dstip,port,local_ip):
        s=self.__sendPackSock(local_ip,dstip,port)
        agent=smc_agent_simulation(local_ip)
        readlist=[s]
        select_time=0
        while True:
            rs,ws,es=select.select(readlist, [], [], 5)
            if rs == []:
                pack=agent.send_pack()
                if type(pack) == tuple :  # status==2， 需要发送两个报文。
                    for i in range(len(pack)):
                        s.send(pack[i])
                else :
                    s.send(pack)
            else:
                message=s.recv(8192)
                pack=agent.unpack_header(message)
                if type(pack) == tuple :
                    for i in range(len(pack)):
                        s.send(pack[i])
                else :
                    s.send(pack)
                    
            try:
                status=que.get(block=False)
                if 'showlicense' in status :
                    wait_license_time=0
                    while not hasattr(agent,'license'):
                        if wait_license_time > status['showlicense']['time']:
                            raise
                        time.sleep(1)
                        wait_license_time+=1
                    que.put(agent.license)
                elif 'pause' in status :
                    pause_time=status['pause']['time']   
                    time.sleep(pause_time)
            except :
                pass
            
    def __agent_start(self):
        pro=process(target=self.__agent_simulation(self.que, self.targetip, self.targetport, self.localip, ))
        pro.daemon=True
        pro.start()
        pro.join()
        return pro

class smc_agent_simulation():  #vfw 实例
    status=0
    sessionID=0
    runTime=time.time()
    smcRunTime=time.time()
    def __init__(self,ip):
        self.ip=ip
        self.sn='10076-0023I-{:e<5}-E404P-{:x<5}'.format(random.randint(1,1000),ip.split('.')[-1])
        
    def _pack_header(self):
        sequence=2
        reserved=0
        version=2
        timestamp=time.time()
        header=struct.pack('!HbbHHif',version,self.command[0],self.command[1],sequence,reserved,self.sessionID,timestamp)
        return header
    
    def unpack_header(self,data):
        command=[0,0]
        if len(data) == 16 :
            ver,command[0],command[1],sequence,reserved,sessionID,timestamp=struct.unpack('!HbbHHif',data)
        else :
            ver,command[0],command[1],sequence,reserved,sessionID,timestamp,cloud_data=struct.unpack('!HbbHHif%ds'%(len(data)-16),data)
        if  command == [1,2] :  # 绑定应答报文
            self.sessionID=sessionID
            self.status = 1 #云端给绑定做应答，下次发送请求license
        elif command == [6,2] :  # update 
            self.license = cloud_data.decode('utf-8')
            self.status = 2  #license 更新后，只发送keepalive
        elif command == [6,3]: #收到云端发送的报活keepalive
            self.smcRunTime=time.time()  #收到smc的应答报文，更新smc在线时间。
            #pass
        return self.send_pack()
            
    def _send_bindcode(self):
        self.command=[1,1]
        data='{"sn": "'+self.sn+'", "bindCode": "aed995e7ce694c4287d9cd512e3d3229"}'
        return self._pack_header()+data.encode('ascii')
        
    def _send_licence_request(self):
        self.command=[6,1]
        self.core='{"core": "4"}'
        return self._pack_header()+self.core.encode('ascii')
    def _send_device_notice(self):  #agent keepalive
        self.command=[2,1]
        if self.status == 2 :
            dev_info='{"hostName": "'+self.ip+'", "hostIP": "'+self.ip+'", "version": "V1.1-R2.120161212", "uptime": "'+str(int(time.time()-self.runTime))+'", "cpuInfo": {"total": "100.00", "used": "0.00"}, "memInfo": {"total": "1096636116", "used": "455400072"}, "nrConns": "30", "nrUsers": "52", "cycle": "10", "license": '+self.license+'}'
        else :
            dev_info='{"hostName": "'+self.ip+'", "hostIP": "'+self.ip+'", "version": "V1.1-R2.120161212", "uptime": "'+str(int(time.time()-self.runTime))+'", "cpuInfo": {"total": "100.00", "used": "0.00"}, "memInfo": {"total": "1096636116", "used": "455400072"}, "nrConns": "30", "nrUsers": "52", "cycle": "10"}'
        return self._pack_header()+dev_info.encode('ascii')
        
    def send_pack(self):
        if int(time.time()-self.smcRunTime) > 300 :  #smc长时间不发送keepalive报文，则认为smc不在线，重新请求绑定。
            self.status=0
        if self.status == 0 : # 请求绑定
            return self._send_bindcode()
        elif self.status == 1:  # 请求license
            return self._send_licence_request(),self._send_device_notice()
        elif self.status == 2: # 只发送keepalive
            return self._send_device_notice
        
if __name__ == '__main__':
    agent=agent_simulation('127.0.0.1','127.0.0.1',9070)
    pdb.set_trace()
    agent.set_status('start')
    agent.set_status('restart')
    agent.set_status('pause',time=10)
    agent.set_status('showlicense',time=10)
    agent.set_status('stop')