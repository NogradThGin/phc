#!/usr/bin/env python3

from .commands  import *
from sys       import argv

from argparse  import ArgumentParser, REMAINDER


if __name__ == "__main__":
    parser = ArgumentParser(description='Proxmox Home Cloud remote manager')
    parser.add_argument('type', choices=['machine', 'ip', 'dns', 'ca', 'git', 'test'], nargs=REMAINDER)
    args = parser.parse_args()

    argv.remove(argv[0])
    func = f'{argv[0]}_{argv[1]}'
    argv.remove(argv[0])

    locals()[func]()