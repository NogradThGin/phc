from requests import post, delete, get
from time     import sleep


class PROXMOX:
    def __init__(self, conf:dict, node:str):
        self.__conf = conf

        self.__uri = f'https://{self.__conf["uris"]["proxmox"]}/api2'
        self.__ca = self.__conf["network"]["ca_cert"]

        self.__headers = {'Authorization': self.__conf['tokens']['proxmox']}

        self.__node = node


    def list_vms(self):
        url = f'{self.__uri}/json/cluster/resources/'
        r = get(url, headers=self.__headers, verify=self.__ca)

        for item in r.json()['data']:
            if item['type'] == 'qemu':
                if item['template'] == 0:
                    yield item


    def next_available_id(self):
        url = f'{self.__uri}/json/cluster/nextid'
        r = get(url, headers=self.__headers, verify=self.__ca)

        return r.json()['data']


    def get_vm_id(self, vm_name):
        url = f'{self.__uri}/json/nodes/{self.__node}/qemu/'
        r = get(url, headers=self.__headers, verify=self.__ca)

        __ret_data = None

        for vm in r.json()['data']:
            if vm['name'] == vm_name and not __ret_data:
                __ret_data = vm['vmid']

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': __ret_data})
        else:
            return ({'status': False, 'data': r.text})


    def get_vm_ip(self, vm_id):
        url = f'{self.__uri}/json/nodes/{self.__node}/qemu/{vm_id}/config'
        r = get(url, headers=self.__headers, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.json()['data']['ipconfig0'].split(',')[0].split('=')[1]})
        else:
            return ({'status': False, 'data': r.text})


    def clone(self, name:str, source:int=9999, target:int=9999, full_clone:bool=True):
        params = {
            'newid': target,
            'name': name,
            'target': self.__node,
            'full': int(full_clone),
        }

        url = f'{self.__uri}/json/nodes/{self.__node}/qemu/{source}/clone'
        r = post(url, params=params, headers=self.__headers, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.text})
        else:
            return ({'status': False, 'data': r.text})


    def delete(self, id:int):
        url = f'{self.__uri}/json/nodes/{self.__node}/qemu/{id}'
        r = delete(url, headers=self.__headers, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.text})
        else:
            return ({'status': False, 'data': r.text})


    @property
    def node(self):
        return self.__node

    @node.setter
    def node(self, value):
        self.__node = value