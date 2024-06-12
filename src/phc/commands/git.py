from ..generic   import read_config, sjprint, jprint
from ..objects   import git

from argparse    import ArgumentParser
from sys         import _getframe

conf = read_config()

def git_create():
    parser = ArgumentParser(description='Proxmox Home Cloud remote manager', prog=_getframe().f_code.co_name.replace('_', ' '))
    parser.add_argument("repo", type=str, help="Repository to manage")
    args, unknown = parser.parse_known_args()

    header = ['NAME', 'REPOSITORY', 'MAIN BRANCH', '# BRANCH', 'STATUS']
    repo = git(conf, args.repo)

    ret = repo.create()['data']
    repo_infos = repo.get_infos()['data']

    branch_default = repo_infos['branch']['default']
    branch_count   = repo_infos['branch']['count']
    repo_name      = args.repo
    requested_repo = repo_infos['name']

    content = [repo_name, requested_repo, branch_default, branch_count, ret]

    sjprint(header=header, content=content)


def git_delete():
    parser = ArgumentParser(description='Proxmox Home Cloud remote manager', prog=_getframe().f_code.co_name.replace('_', ' '))
    parser.add_argument("repo", type=str, help="Repository to manage")
    args, unknown = parser.parse_known_args()

    header = ['NAME', 'REPOSITORY', 'MAIN BRANCH', '# BRANCH', 'STATUS']
    justifier = 20

    jprint(content=header)

    repo = git(conf, args.repo)
    ret = repo.get_status()['data']
    
    repo_infos = repo.get_infos()['data']
    ret = repo.delete()['data']

    branch_default = repo_infos['branch']['default']
    branch_count   = repo_infos['branch']['count']
    repo_name      = args.repo
    requested_repo = repo_infos['name']

    content = [repo_name, requested_repo, branch_default, branch_count, ret]
    jprint(content=content)


def git_info():
    parser = ArgumentParser(description='Proxmox Home Cloud remote manager', prog=_getframe().f_code.co_name.replace('_', ' '))
    parser.add_argument("repo", type=str, help="Repository to get informations from")
    args, unknown = parser.parse_known_args()

    header = ['NAME', 'REPOSITORY', 'MAIN BRANCH', '# BRANCH', 'STATUS']
    justifier = 20

    repo = git(conf, args.repo)
    repo_infos = repo.get_infos()['data']

    branch_default = repo_infos['branch']['default']
    branch_count   = repo_infos['branch']['count']
    repo_name      = args.repo
    requested_repo = repo_infos['name']
    ret            = repo_infos['status']

    content = [repo_name, requested_repo, branch_default, branch_count, ret]

    sjprint(content=content, header=header)


def git_list():
    parser = ArgumentParser(description='Proxmox Home Cloud remote manager', prog=_getframe().f_code.co_name.replace('_', ' '))
    args, unknown = parser.parse_known_args()

    header = ['NAME', 'REPOSITORY', 'MAIN BRANCH', '# BRANCH', 'STATUS']
    justifier = 20

    repo = git(conf, None)
    repo_list = repo.get_list()

    jprint(content=header)

    for itr_repo in repo_list['data']:
        repo.repo = itr_repo
        repo_infos = repo.get_infos()['data']

        branch_default = repo_infos['branch']['default']
        branch_count   = repo_infos['branch']['count']
        repo_name      = itr_repo
        requested_repo = repo_infos['name']
        ret            = repo_infos['status']

        content = [itr_repo, repo_infos['name'], repo_infos['branch']['default'], repo_infos['branch']['count'], ret]
        jprint(content=content)