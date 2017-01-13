# -*- coding:utf-8 -*-  

import requests
import sys
import urlparse
import multiprocessing
import BaseHTTPServer
import time

from lib.public import _searchchar,ExpectError

class _WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """
        """
        self.protocol_version='HTTP/1.1'
        msgs='WAF test!'
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                '<html>',
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                'message=%s' % msgs,
                '',
                'HEADERS RECEIVED:',
                ]
        self.send_response(200)
        
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('</html>')
        message = '\r\n'.join(message_parts)
        self.send_header('Content-Length',str(len(message)))
        self.send_header('Content-Type','text/html')
        self.end_headers()
        self.wfile.write(message)

    def do_PSOT(self):
        """
        """
        self.protocol_version='HTTP/1.1'
        msgs='WAF test!!!\n'
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
                '<html>',
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                'message=%s' % msgs,#.decode('utf-8').encode('gbk'),
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('</html>')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Length',str(len(message)))
        self.send_header('Content-Type','text/html')
        self.end_headers()
        self.wfile.write(message)
        
class http_serv(object):
    """docstring for http_keyword"""
    serProcess=[]

    def _http_serv_simple(self,ip='0.0.0.0',port=80):
        port=int(port)
        server = BaseHTTPServer.HTTPServer((ip,port), _WebRequestHandler)
        server.serve_forever()

    def http_serv(self,ip='0.0.0.0',port=80):
        '''
            http_cli action get: "测试！！！！！！！！"、"test"、"邪教"、"さしす"
            http_cli action post: "测试！！！！！！！！"
        '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        process=multiprocessing.Process(target=self._http_serv_simple,args=(ip,port,))
        process.daemon=False
        process.start()
        http_serv_pid=process.pid
        self.serProcess.append(process)
        print("http server {ip}:{port} pid {pid} is starting~".format(ip=ip,port=port, pid=http_serv_pid))

    def http_serv_stop(self):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        while len(self.serProcess) != 0 :
            http_serv_pid=self.serProcess[-1].pid
            self.serProcess[-1].terminate()
            #self.serProcess[-1].join()
            del self.serProcess[-1]
            print("http server pid {} is killed~".format(http_serv_pid))
        
#         for i in range(len(self.serProcess))[::-1]:
#             self.serProcess[i].terminate()
#             self.serProcess[i].join()
#             del self.serProcess[i]
#             print("http server is killed~")

class http_cli(object):
    def __init__(self):
        pass
    
    def http_cli(self,url='',expect=1,searchc=None,status_code=None):
        '''
        '''
        print("run keyword : {}  {}".format(sys._getframe().f_code.co_name,locals()))
        
        try:
            req=requests.get(url=url)
        except:
            if expect == 0 or expect == '0':
                if searchc ==None or str(searchc) == 'None' or searchc == '':
                    print("expect get url from host:%s fail, actually fail"%url)
                else :
                    raise ExpectError("expect get url from host:%s ,connect fail"%url)
            else :
                raise ExpectError("get url from host:%s error!"%url)
        else:
            html_text=req.text
            if ( expect == 1 or expect == '1' ) and ( status_code == None or int(status_code) == req.status_code ) :
                print("expect get url from host:%s success, actually sucess , status_code %s"%(url,str(status_code)))
                if searchc !=None and str(searchc) != 'None' and searchc != '' :
                    _searchchar(searchc,html_text,expect,'http')                    
            elif ( expect == 1 or expect == '1' ) and req.status_code != str(status_code) :
                #print("body:",html_text)
                raise ExpectError("expect get url from host:%s status_code error, expect %s ; actually %s"%(url,status_code,req.status_code))
            elif ( expect == '0' or expect == 0 ) :
                raise ExpectError("expect get url from host:%s fail, actually success"%url)




if __name__ == '__main__' :
    serv=http_serv()
    serv.http_serv(port=8008)
    serv.http_serv(port=8001)
    serv.http_serv(port=8002)
#     hosthttp=http_cli()
#     hosthttp.http_cli(url='http://172.17.21.110',expect=1,searchc='body')
#     hosthttp.http_cli(url='http://172.17.21.110',expect=1)
#     hosthttp.http_cli(url='http://172.17.20.1:8008',expect=1)
#     hosthttp.http_cli(url='http://172.17.20.1:8008/abc/text/',expect=1,status_code=200)
#     hosthttp.http_cli(url='http://127.0.0.1:8008/abc?abc=1&cde=2',expect=1,status_code=200)
#     hosthttp.http_cli(url='http://172.17.21.99',expect=0)
    serv.http_serv_stop()
    

