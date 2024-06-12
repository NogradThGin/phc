from paramiko        import AutoAddPolicy
from paramiko.client import SSHClient


class CA:
    def __init__(self, conf:dict):
        self.__conf = conf

    def create_ca(self, vm_name:str):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(self.__conf['uris']['ca'], username=self.__conf['network']['ca_ssh_user'], key_filename=self.__conf['network']['ca_ssh_key'])
        _stdin, _stdout,_stderr = client.exec_command(f"/home/admin/auto.sh {vm_name}")
        client.close()

        return ({'status': True, 'data': f"Please check on server /etc/ssl/private/{vm_name}.key and /etc/ssl/certs/{vm_name}.crt presence"})


    def delete_ca(self, vm_name:str):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(self.__conf['uris']['ca'], username=self.__conf['network']['ca_ssh_user'], key_filename=self.__conf['network']['ca_ssh_key'])
        _stdin, _stdout,_stderr = client.exec_command(f"/home/admin/del.sh {vm_name}")
        client.close()

        return ({'status': True, 'data': ""})
