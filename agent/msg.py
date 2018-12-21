import uuid
import os
import socket
import datetime
import netifaces
import ipaddress
from .config import *


class Message:
    def __init__(self, myidpath):
        self.id = ""
        if os.path.exists(myidpath):
            with open(myidpath, encoding="utf-8") as f:
                id = f.readline().strip()
                if len(id) == 32:
                    self.id = id

        if not self.id:  # 如果没有去到ID
            self.id = uuid.uuid4().hex
            with open(myidpath, 'w', encoding="utf-8") as f:
                f.write(self.id)
        # print(self.id)

    def _get_addresses(self):
        """获取主机上所有的包括私有的IPV4地址列表"""
        address = []

        for ifac in netifaces.interfaces():
            ipv4s = netifaces.ifaddresses(ifac).get(2, [])
            for ip in ipv4s:
                ip = ipaddress.ip_address(ip.get('addr'))
                if ip.version != 4:
                    continue
                if ip.is_link_local: # 169.254地址
                    continue
                if ip.is_loopback:
                    continue
                if ip.is_reserved:
                    continue

                address.append(str(ip))

        return address
        # print(address)

    def reg(self):
        '''生成注册信息'''
        return {
            'id':self.id,
            'hostname': socket.gethostname(),
            'timestamp':datetime.datetime.now().timestamp(),
            'ip':self._get_addresses()

        }

    def heartbeat(self):
        '''生成心跳信息'''
        return {
            'id':self.id,
            'hostname':socket.gethostname(),
            'timestamp':datetime.datetime.now().timestamp(),
            'ip':self._get_addresses()
        }

    def result(self, task_id, code, output):
        return {
            'id':task_id,
            'agent_id':self.id,
            'code':code,
            'output':output
        }




if __name__ == '__main__':
    m = Message(MYID_PATH)
    m._get_addresses()
    print(m.heartbeat())
    print(m.reg())
