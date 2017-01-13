# -*- coding: utf-8 -*-

#from lib.robotremoteserver  import RobotRemoteServer as RemoteServer
from robotremoteserver  import RobotRemoteServer as RemoteServer
import sys

from lib.waf.api import api as waf_api
from lib.pcControl.host_ping import ping
from lib.pcControl.host_networkconfigure import networkconfigure
from lib.pcControl.host_execute import host_execute_cmd
from lib.pcControl.host_http import http_cli
from lib.pcControl.host_http import http_serv
from lib.pcControl.file_transfar import file_keyword
from lib.pcControl.socket_transmission import socket_transmission

class local_library(waf_api, \
                    ping, \
                    networkconfigure, \
                    host_execute_cmd, \
                    http_cli, \
                    http_serv, \
                    file_keyword, \
                    socket_transmission, \
                    ):
    def __init__(self):
        pass

if __name__ == '__main__': 
    RemoteServer(library=local_library(),host='0.0.0.0')
    #RemoteServer(library=local_library,*sys.argv[1:])