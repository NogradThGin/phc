from yaml    import FullLoader, load
from os      import environ
from os.path import isfile, islink
from .errors import ConfigError

def read_config():
    conf_path = str()

    conf_paths = [
            f"{environ['HOME']}/.config/phc/config.yaml",
            f"{environ['HOME']}/.config/phc/config.yml",
            f"{environ['HOME']}/.config/phc.yaml",
            f"{environ['HOME']}/.config/phc.yml",
            f"/etc/phc/config.yaml"
            f"/etc/phc/config.yml"
        ]

    for conf_file in conf_paths:
        if isfile(conf_file) or islink(conf_file):
            conf_path = conf_file
            break

    if conf_path:
        with open(conf_path) as f:
            conf = load(f, Loader=FullLoader)

            if conf['global']['use_network_domain_for_entities']:
                data = {
                    "uris": {
                        "proxmox": f'{conf["entities"]["proxmox"]}.{conf["network"]["domain"]}',
                        "ipam": f'{conf["entities"]["ipam"]}.{conf["network"]["domain"]}',
                        "dns": f'{conf["entities"]["dns"]}.{conf["network"]["domain"]}',
                        "ca": f'{conf["entities"]["ca"]}.{conf["network"]["domain"]}',
                        "git": f'{conf["entities"]["git"]}.{conf["network"]["domain"]}'
                    }
                }
            else:
                data = {
                    "uris": {
                        "proxmox": conf["entities"]["proxmox"],
                        "ipam": conf["entities"]["ipam"],
                        "dns": conf["entities"]["dns"],
                        "ca": conf["entities"]["ca"],
                        "git": conf["entities"]["git"]
                    }
                }
                
        conf.update(data)

        return conf
    else:
        raise ConfigError("No config file found")