from argparse import ArgumentParser
from sys      import argv
from generic  import sjprint

def test():
    parser = ArgumentParser(description='Proxmox Home Cloud remote manager', prog=_getframe().f_code.co_name.replace('_', ' '))
    parser.add_argument("--node", type=str, default="pve", help="Node for the VM to use")
    args, unknown = parser.parse_known_args()

    sjprint("NAME", "NODE", "MACHINE_TYPE", "INTERNAL_IP", "DNS", "STATUS")