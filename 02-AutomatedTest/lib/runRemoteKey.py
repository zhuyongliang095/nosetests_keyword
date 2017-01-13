# -*- coding: utf-8 -*-

from robot.libraries.Remote import Remote

def runRemoteKey(host,name, *args,**kwargs):
    '''可以使用这个关键字在远程机上运行远程机的关键字。
            host=192.168.7.108   远程机的IP和端口。
            name=keyword   在远程机上运行的关键字。
            *args=args   关键字参数，可以是多个，用括号括起来。
                                            你可以在suit的添加全局变量，定义uri。
        '''
    uri_host='uri_'+host.replace('.','_')
    if  uri_host not in globals():
        globals()[uri_host]=Remote('http://'+host+':8270')
    RemoteHost=globals()[uri_host]
    RemoteHost.run_keyword(name, args=args, kwargs = kwargs)
    
if __name__ == '__main__':
    print('abc')
    runRemoteKey('192.168.0.1','test',)
    runRemoteKey('192.168.0.1','test',)