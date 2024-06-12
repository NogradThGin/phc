from requests import post, put, get


class MACHINE:
    def __init__(self, conf:dict, name:str="", ip:str="", id:int=None, node:str='pve'):

        self.__conf = conf

        self.__uri = f'https://{self.__conf["uris"]["proxmox"]}/api2'
        self.__ca = self.__conf["network"]["ca_cert"]
        self.__gw = self.__conf['network']['gateway']

        self.__headers = {'Authorization': self.__conf['tokens']['proxmox']}

        self.__name = name
        self.__ip = ip
        self.__id = id
        self.__node = node


    def stop(self):
        url = f'{self.__uri}/json/nodes/{self.__node}/qemu/{self.__id}/status/stop'
        r = post(url, headers=self.__headers, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.text})
        else:
            return ({'status': False, 'data': r.text})


    def get_status(self):
        url = f'{self.__uri}/json/nodes/{self.__node}/qemu/{self.__id}/status/current'
        r = get(url, headers=self.__headers, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.json()})
        else:
            return ({'status': False, 'data': r.json()})


    def update_ip(self):
        self.__headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        
        data = {'ipconfig0': f'ip={self.__ip},gw={self.__gw}'}

        url = f'{self.__uri}/json/nodes/{self.__node}/qemu/{self.__id}/config'
        r = put(url, headers=self.__headers, data=data, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.text})
        else:
            return ({'status': False, 'data': r.text})


    def start(self):
        url = f'{self.__uri}/json/nodes/{self.__node}/qemu/{self.__id}/status/start'
        r = post(url, headers=self.__headers, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.text})
        else:
            return ({'status': False, 'data': r.text})


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value


    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value


    @property
    def ip_pdns(self):
        return self.__ip_pdns

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, value):
        self.__ip = value
        self.__ip_pdns = value.split('/')[0]