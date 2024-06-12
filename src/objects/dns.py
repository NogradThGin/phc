from requests import patch


class DNS:
    def __init__(self,
                 conf:dict):

        self.__conf = conf

        self.__uri = f'http://{self.__conf["uris"]["dns"]}/api/v1'
        self.__ca = self.__conf["network"]["ca_cert"]

        self.__headers = {'X-API-Key': self.__conf['tokens']['dns']}

    
    def create_record(self, vm_name:str, ip_address:str, type:str="A"):
        json_data = {
  "rrsets": [
    {
      "name": f"{vm_name}.{self.__conf['network']['domain']}.",
      "ttl": "60",
      "type": "A",
      "changetype": "REPLACE",
      "records": [{
          "content": ip_address,
          "disabled": False,
          "name": f"{vm_name}.{self.__conf['network']['domain']}.",
          "type": f"{type}",
          "priority": 0
        },
      ]
    }
  ]
}
        url = f'{self.__uri}/servers/localhost/zones/{self.__conf["network"]["domain"]}.'
        r = patch(url, headers=self.__headers, json=json_data, verify=self.__ca)

        return ({'status': True, 'data': r.text})


    def remove_record(self, vm_name:str, type:str="A"):
        json_data = {
  "rrsets": [
    {
      "changetype": "DELETE",
      "type": f"{type}",
      "name": f"{vm_name}.local.net."
    }
  ]
}
        url = f'{self.__uri}/servers/localhost/zones/{self.__conf["network"]["domain"]}.'
        r = patch(url, headers=self.__headers, json=json_data, verify=self.__ca)

        return ({'status': True, 'data': r.text})


    def get_record_ip(self, vm_name:str):
        url = f'{self.__uri}/servers/localhost/zones/{self.__conf["network"]["domain"]}.'
        r = patch(url, headers=self.__headers, json=json_data, verify=self.__ca)

        return ({'status': True, 'data': r.text})
