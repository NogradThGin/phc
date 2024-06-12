from requests import delete, put, get

class GIT:
    def __init__(self, conf:dict, repo_name:str, default_branch:str="master"):
        self.__conf = conf
        self.__repo_name = repo_name

        self.__conf = conf

        self.__uri = f'https://{self.__conf["uris"]["git"]}'
        self.__ca = self.__conf["network"]["ca_cert"]

        self.__headers = {'Authorization': f'Bearer {self.__conf["tokens"]["git"]}'}
        self.__data_type = None
        self.__default_branch = default_branch


    def create(self):
        json_data = {"repo": self.__repo_name, "default_branch": self.__default_branch}

        url = f'{self.__uri}/create'
        r = put(url, headers=self.__headers, json=json_data, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.text})
        else:
            return ({'status': False, 'data': r.text})

    def delete(self):
        json_data = {"repo": self.__repo_name}

        url = f'{self.__uri}/delete'
        r = delete(url, headers=self.__headers, json=json_data, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.text})
        else:
            return ({'status': False, 'data': r.text})


    def get_infos(self):
        json_data = {
            'repo': self.__repo_name,
            'type': self.__data_type,
        }
        url = f'{self.__uri}/info'
        r = get(url, headers=self.__headers, json=json_data, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.json()})
        else:
            return ({'status': False, 'data': r.text})


    def get_status(self):
        json_data = {
            'repo': self.__repo_name,
        }
        
        url = f'{self.__uri}/status'
        r = get(url, headers=self.__headers, json=json_data, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.text})
        else:
            return ({'status': False, 'data': r.text})


    def get_list(self):
        url = f'{self.__uri}/list'
        r = get(url, headers=self.__headers, verify=self.__ca)

        if r.status_code >= 200 and r.status_code < 300:
            return ({'status': True, 'data': r.json()})
        else:
            return ({'status': False, 'data': r.text})


    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, value):
        self.__data_type = value

    @property
    def repo(self):
        return __repo_name

    @data_type.setter
    def repo(self, value):
        self.__repo_name = value
