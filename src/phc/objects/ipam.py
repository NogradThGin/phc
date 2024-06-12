from random   import randint
from requests import get, post, patch, delete


class IPAM:
    def __init__(self,
                 conf:dict):

        self.__conf = conf

        self.__uri = f'https://{self.__conf["uris"]["ipam"]}/api'
        self.__ca = self.__conf["network"]["ca_cert"]

        self.__headers = {'Authorization': f"Token {self.__conf['tokens']['ipam']}"}

        self.__randomized = int((len(str(999))-len(str(randint(0, 999))))*'0'+str(randint(0, 999)))


    def next_available_ip(self, limit:int=1000):
        params = {
            'limit': limit,
        }

        r = get(f'{self.__uri}/ipam/ip-ranges/1/available-ips/', params=params, headers=self.__headers, verify=self.__ca)

        return ({'status': True, 'data': r.json()[self.__randomized]['address']})

    
    def get_vm_ip_address(self, vm_name:str):
        self.__headers.update({'accept': 'application/json', 'Content-Type': 'application/json'})

        params = {
            'name': vm_name,
        }

        r = get(f'{self.__uri}/virtualization/virtual-machines/', params=params, headers=self.__headers, verify=self.__ca)

        data = r.json()

        if int(data['count']) > 1:
            return ({'status': True, 'data': "More than one result!"})
        elif int(data['count']) == 0:
            return ({'status': True, 'data': "No results!"})
        else:
            return ({'status': True, 'data': r.json()['results'][0]['primary_ip']['address']})


    def create_virtual_machine(self, vm_name:str):
        json_data = {
            'name': vm_name,
            'site': 1,
            'cluster': 1,
            'tenant': 1,
            'vcpus': 1,
            'memory': 2048,
            'disk': 20,
        }

        r = post(f'{self.__uri}/virtualization/virtual-machines/', headers=self.__headers, json=json_data, verify=self.__ca)

        return ({'status': True, 'data': r.json()['id']})


    def create_interface(self, int_name:str, vm_id:str):
        json_data = {
            'name': int_name, 
            'virtual_machine': str(vm_id)
        }

        r = post(f'{self.__uri}/virtualization/interfaces/', headers=self.__headers, json=json_data, verify=self.__ca)

        return ({'status': True, 'data': r.json()['id']})


    def create_disk(self, disk_name:str, size_gb:int, vm_id:str):
        json_data = {
            'name': disk_name, 
            'virtual_machine': str(vm_id),
            'size': size_gb,
        }

        r = post(f'{self.__uri}/virtualization/virtual-disks/', headers=self.__headers, json=json_data, verify=self.__ca)

        return ({'status': True, 'data': r.json()['id']})


    def create_ip_address(self, vm_name:str, ip_address:str, interface_id:str):
        json_data = {
            'address': ip_address, 
            'assigned_object_id': interface_id,
            'assigned_object_type': 'virtualization.vminterface',
            'dns_name': f'{vm_name}.{self.__conf["network"]["domain"]}',
            'site': 1,
            'cluster': 1,
            'tenant': 1,
        }

        r = post(f'{self.__uri}/ipam/ip-addresses/', headers=self.__headers, json=json_data, verify=self.__ca)

        return ({'status': True, 'data': r.json()['id']})


    def attach_ip_address_to_virtual_machine(self, ip_address:str, vm_id:str):
        json_data = {
            'primary_ip4': {
                'address': ip_address
            },
        }

        r = patch(f'{self.__uri}/virtualization/virtual-machines/{vm_id}/', headers=self.__headers, json=json_data, verify=self.__ca)

        return ({'status': True, 'data': r.json()['id']})

    
    def get_vm_disk_id(self, vm_name:str):
        self.__headers.update({'accept': 'application/json', 'Content-Type': 'application/json'})

        params = {
            'virtual_machine': vm_name,
        }

        r = get(f'{self.__uri}/virtualization/virtual-disks/', params=params, headers=self.__headers, verify=self.__ca)

        try:
            return ({'status': True, 'data': r.json()['results'][0]['id']})
        except:
            return ({'status': True, 'data': r.text})

    
    def get_vm_interface_id(self, vm_name:str):
        self.__headers.update({'accept': 'application/json', 'Content-Type': 'application/json'})

        params = {
            'virtual_machine': vm_name,
        }

        r = get(f'{self.__uri}/virtualization/interfaces/', params=params, headers=self.__headers, verify=self.__ca)

        try:
            return ({'status': True, 'data': r.json()['results'][0]['id']})
        except:
            return ({'status': True, 'data': r.text})

    
    def get_vm_ip_address_id(self, vm_name:str):
        self.__headers.update({'accept': 'application/json', 'Content-Type': 'application/json'})

        params = {
            'virtual_machine': vm_name,
        }

        r = get(f'{self.__uri}/ipam/ip-addresses/', params=params, headers=self.__headers, verify=self.__ca)

        try:
            return ({'status': True, 'data': r.json()['results'][0]['id']})
        except:
            return ({'status': True, 'data': r.text})

    
    def get_vm_id(self, vm_name:str):
        self.__headers.update({'accept': 'application/json', 'Content-Type': 'application/json'})

        params = {
            'name': vm_name,
        }

        r = get(f'{self.__uri}/virtualization/virtual-machines/', params=params, headers=self.__headers, verify=self.__ca)

        try:
            return ({'status': True, 'data': r.json()['results'][0]['id']})
        except:
            return ({'status': True, 'data': r.text})


    def delete_vm(self, vm_id:str):
        r = delete(f'{self.__uri}/virtualization/virtual-machines/{vm_id}/', headers=self.__headers, verify=self.__ca)

        return ({'status': True, 'data': r.text})


    def delete_ip(self, ip_id:str):
        r = delete(f'{self.__uri}/ipam/ip-addresses/{ip_id}/', headers=self.__headers, verify=self.__ca)

        return ({'status': True, 'data': r.text})


    def delete_disk(self, disk_id:str):
        r = delete(f'{self.__uri}/virtualization/virtual-disks/{disk_id}/', headers=self.__headers, verify=self.__ca)

        return ({'status': True, 'data': r.text})


    def delete_interface(self, interface_id:str):
        r = delete(f'{self.__uri}/virtualization/interfaces/{interface_id}/', headers=self.__headers, verify=self.__ca)

        return ({'status': True, 'data': r.text})