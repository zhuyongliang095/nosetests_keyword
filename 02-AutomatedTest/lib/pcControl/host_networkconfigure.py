# -*- coding:utf-8 -*-  
import subprocess
import re
import sys
import platform
import chardet
import time

from lib.public import _searchchar
from lib.public import ExpectError
from lib.public import _char2uni
from lib.public import local_system
from etc.read_conf import waf

class networkconfigure(object):
    def __init__(self):
        pass

    def __exchange_mask_to_int(self,mask):
        count_bit = lambda bin_str: len([i for i in bin_str if i=='1'])
        mask_splited = mask.split('.')
        mask_count = [count_bit(bin(int(i))) for i in mask_splited]
        return sum(mask_count)

    def __exchange_int_to_mask(self,mask_int):
        bin_arr = ['0' for i in range(32)]
        for i in range(mask_int):
            bin_arr[i] = '1'
        tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
        tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
        return '.'.join(tmpmask)
    
    def __exchage_mask(self,mask):
        if 'Linux' in local_system:
            if isinstance(mask,int) :
                return mask
            else :
                return self.__exchange_mask_to_int(mask)
        else :
            if isinstance(mask,int) :
                return self.__exchange_int_to_mask(mask)
            else :
                return mask

    def _get_inter_id(self,inter_name='test'):
        if 'Linux' in local_system :
            cmd='ifconfig -a'
        elif 'Windows' in local_system :
            if 7 > local_system['Windows'] :
                cmd='netsh interface ip show interface '+str(inter_name)
            elif 7 <= local_system['Windows'] :
                cmd='netsh interface ipv4 show interface '
        msgs=self._run_cmd(cmd)
        if re.search('2003',platform.release()) :
            return msgs[0].split('------------------------------------------------------')[1].split('\n')[1].split(':')[1]
        else:
            msgs_tem=[]
            for i in range(len(msgs)):
                msgs_tem.extend(msgs[i].split('\n'))
            for line in msgs_tem:
                if inter_name in line:
                    return line.split()[0]
    
    def _run_cmd(self,cmd):
        print("{}".format(cmd))
        msgs=[]
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        if 'Windows' in local_system :
            p.terminate()
        return '\n'.join(_char2uni(msgs))
        
    def show_ip(self,inter='test',searchip=None,ip_type=4,times=15):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        if int(ip_type) == 4 or int(ip_type) == 6 :
            ip_type=int(ip_type)
        else:
            raise ExpectError("ip type error")
        
        if 'Linux' in local_system : 
            cmd='ip addr show {inter}'.format(inter=inter)
        elif 'Windows' in local_system :
            if int(ip_type) == 4:
                if 7 > local_system['Windows'] :
                    cmd='netsh interface ip show config "'+inter+'"'
                elif 7 <= local_system['Windows'] :
                    cmd='netsh interface ipv4 show address "'+inter+'"'
            else:
                cmd='ipconfig'
        tm=0
        #cmd='ipconfig'
        for i in range(int(times)):
            try :
                msgs=self._run_cmd(cmd)
                return _searchchar(searchip,msgs,expect=1,tpye='pc')
            except  :
                raise 
                tm+=1
                time.sleep(1)
                if tm == int(times):
                    raise ExpectError("search ip %s error"%searchip)
                else:
                    print("search times %d, search error"%tm)

    def static_ip_add(self,inter='test',ip=None,netmask=None):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        netmask=self.__exchage_mask(netmask)
        if 'Linux' in local_system : 
            cmd='ip addr add {ip}/{netmask} dev {inter}'.format(inter=inter,ip=ip,netmask=netmask)
        elif 'Windows' in local_system :
            if int(ip_type) == 4:
                if 7 < local_system['Windows'] :
                    cmd='netsh interface ip add address "'+inter+'" '+ip+' '+netmask
                elif 7 >= local_system['Windows']:
                    cmd='netsh interface ipv4 add address "'+inter+'" '+ip+' '+netmask
            else:
                cmd='ipconfig'
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip(inter=inter,searchip=ip)
        
    def static_gw_add(self,inter='test',gw=None,ip_type=4,metric=1):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        if int(ip_type) != 4 and int(ip_type) != 6 :
            raise ExpectError("ip type error")
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd='route add default gw {gw}'.format(gw=gw)
        elif 'Windows' in local_system :
            if int(ip_type) == 4:
                if 7 < local_system['Windows'] :
                    cmd='netsh interface ip add address "'+str(inter)+'" gateway='+str(gw)+' gwmetric='+str(metric)
                elif 7 >= local_system['Windows']:
                    cmd='route add 0.0.0.0/0 '+str(gw)+ ' metric '+str(metric)+' if ' + self._get_inter_id(inter)
            else:
                cmd='route -6 add ::/0 '+str(gw)

        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        if 'Linux' in local_system : 
            cmd='route -n'
            msgs=self._run_cmd(cmd)
            print(msgs)
        else :
            self.show_ip(inter=inter,searchip=gw,ip_type=ip_type)
        
    def static_gw_del(self,inter='test',gw=None,ip_type=4):
        """
        inter : the name of interface in PC
        gw : gateway
        ip_type : type of ip  is 4(ipv4) or 6(ipv6)
        eg:
        | win_gw_del | inter | gw | ip_type |
        """
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        if int(ip_type) != 4 and int(ip_type) != 6 :
            raise ExpectError("ip type error")
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd='route del default'
        elif 'Windows' in local_system :
            if int(ip_type) == 4:
                cmd='route delete 0.0.0.0/0'
            else :
                cmd='route -6 delete ::/0'
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip(inter=inter,searchip=None,ip_type=ip_type)
        
    def static_ip_del(self,inter='test',ip=None,netmask=24,ip_type=4):
        """
        del ip from interface, ip_type is 4(ipv4) or 6(ipv6).
        eg:
        | Win Ip Del | inter | ip | ip_type |
        """
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        netmask=self.__exchage_mask(netmask)
        if int(ip_type) != 4 and int(ip_type) != 6 :
            raise ExpectError("ip type error")
        
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd='ip addr del '+ str(ip)+'/'+str(netmask)+' dev '+ str(inter)
        elif 'Windows' in local_system :
            if 7 > local_system['Windows'] :
                if int(ip_type) == 4:
                    cmd='netsh interface ip delete address "'+str(inter)+'" addr='+ip+' gateway=all'
                else :
                    cmd=''
            elif 7 <= local_system['Windows'] :
                directly_route=ip.split('::')[0]+'::/64'
                ip=ip.split('/')[0]
                cmd='netsh interface ipv6 delete route '+directly_route+' "'+inter +'"  && netsh interface ipv6 delete address "'+str(inter)+'" '+ip
        
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip(inter=inter,searchip=None,ip_type=ip_type)

    def set_dhcp_ip(self,inter='test',searchip=None,ip_type=4,times=30):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name))
        if int(ip_type) != 4 and int(ip_type) != 6 :
            raise ExpectError("ip type error")
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd=''
        elif 'Windows' in local_system :
            if 7 > local_system['Windows'] :
                if int(ip_type) == 4:
                    cmd='netsh interface ip set address name="'+inter+'" source=dhcp'
                else :
                    cmd=''
            elif 7 <= local_system['Windows'] :
                cmd='netsh interface ipv4 set address name="'+str(inter)+'" source=dhcp '

        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip(inter,searchip,ip_type,times)
    
    def dhcp_ip_renew(self,inter='test',searchip=None,ip_type=4,times=30):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        if int(ip_type) != 4 and int(ip_type) != 6 :
            raise ExpectError("ip type error")
        if 'Linux' in local_system :
            cmd=''
        elif 'Windows' in local_system :
            cmd='ipconfig /renew'
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip(inter,searchip,ip_type,times)
    
    def dhcp_ip_release(self ):
        ''' dhcp release        
        '''
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        if int(ip_type) != 4 and int(ip_type) != 6 :
            raise ExpectError("ip type error")
        if 'Linux' in local_system :
            cmd=''
        elif 'Windows' in local_system :
            cmd='ipconfig /release'
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip()
        
    def set_static_ip(self,inter='test',ip=None,netmask='255.255.255.0',ip_type=4 ):
        '''if ip_type = 4 ,netmask = 255.255.255.0 like.
        if ip_type = 6 ,netmask = 2000:1::/64 like this.
        '''
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        netmask=self.__exchage_mask(netmask)
        if int(ip_type) != 4 and int(ip_type) != 6 :
            raise ExpectError("ip type error")
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd='ip addr add '+ip+'/'+netmask+' dev '+inter
        elif 'Windows' in local_system :
            if 7 > local_system['Windows'] :
                if int(ip_type) == 4:
                    cmd='netsh interface ip set address name="'+inter+'" static '+ip+' '+netmask
                else :
                    cmd='netsh interface ipv6 set address "'+inter+'" '+ip+' store=active && netsh interface ipv6 add route '+netmask+' "'+inter+'"'
            elif 7 <= local_system['Windows'] :
                cmd='netsh interface ipv4 set address name="'+inter+'" static '+ip+' '+netmask
        
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip(inter=inter,searchip=ip,ip_type=ip_type)
    
    def set_dhcp_dns(self,inter='test',search_dns=None):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd=''
        elif 'Windows' in local_system :
            if 7 > local_system['Windows'] :
                if int(ip_type) == 4:
                    cmd='netsh interface ip set dns  name="'+inter+'" source=dhcp'
                else :
                    cmd=''
            elif 7 <= local_system['Windows'] :
                cmd='netsh interface ipv4 set dnsservers name="'+inter+'" source=dhcp'
                
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip(inter=inter,searchip=search_dns)
    
    def set_static_dns(self,inter='test',dns_ip=None ):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd=''
        elif 'Windows' in local_system :
            if 7 > local_system['Windows'] :
                if int(ip_type) == 4:
                    cmd='netsh interface ip set dns  name="'+inter+'" source=static '+dns_ip
                else :
                    cmd=''
            elif 7 <= local_system['Windows'] :
                cmd='netsh interface ipv4 set dnsservers name="'+inter+'" static '+dns_ip
        print("{}".format(cmd))
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip(inter=inter,searchip=dns_ip)

    def static_del_dns(self,inter='test',dns_ip='all' ):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd=''
        elif 'Windows' in local_system :
            if 7 > local_system['Windows'] :
                if int(ip_type) == 4:
                    cmd='netsh interface ip delete dns "'+inter+'" '+dns_ip
                else :
                    cmd=''
            elif 7 <= local_system['Windows'] :
                cmd='netsh interface ipv4 delete dnsservers "'+inter+'" '+dns_ip
        print("{}".format(cmd))
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))
        self.show_ip(inter=inter)
        
    def clean_arp(self,inter='test',ip_type=4):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name,locals()))
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd=''
        elif 'Windows' in local_system :
            if 7 > local_system['Windows'] :
                if int(ip_type) == 4:
                    cmd='netsh interface ip delete arpcache name="'+inter+'"'
                else :
                    cmd='netsh interface ipv6 delete neighbors "'+inter+'"'
            elif 7 <= local_system['Windows'] :
                cmd='netsh interface ipv4 delete arpcache "'+inter+'"'
        print("{}".format(cmd))
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))

    def clean_dns_cache(self ):
        print("run keyword : {} ({})".format(sys._getframe().f_code.co_name ))
        if 'Linux' in local_system : 
            if int(ip_type) == 4:
                cmd=''
        elif 'Windows' in local_system :
            if 7 > local_system['Windows'] :
                if int(ip_type) == 4:
                    cmd='ipconfig /flushdns'
                else :
                    cmd=''
            elif 7 <= local_system['Windows'] :
                cmd='ipconfig /flushdns'
        print("{}".format(cmd))
        msgs=self._run_cmd(cmd)
        print("{}".format(msgs))

if __name__ == '__main__':
    test=networkconfigure()
    test.show_ip('eth0','172.17.21.111')
    test.static_ip_add(waf.client_test_interface,'4.4.4.4','24')
    test.static_gw_del(waf.client_test_interface)
    test.static_gw_add(waf.client_test_interface,'172.17.0.1')
    test.static_ip_del(waf.client_test_interface,'4.4.4.4/24')
    