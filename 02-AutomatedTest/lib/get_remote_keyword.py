from robot.libraries.Remote import Remote
import time

def runkey(*args,**kwargs):
    rem=Remote(uri='http://172.17.21.111:8270')
    print('rem ',rem)
    keywork_name=rem.get_keyword_names()
    print(keywork_name)
    rem.run_keyword('http_serv',args=args,kwargs=kwargs)
    #time.sleep(60)
    #rem.run_keyword('stop_remote_server',args=args,kwargs=kwargs)
    rem.run_keyword('http_serv_stop',args=args,kwargs=kwargs)

if __name__ == '__main__' :
    runkey()