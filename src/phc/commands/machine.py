from ..generic  import read_config, sjprint
from ..objects  import *

from argparse   import ArgumentParser
from sys        import _getframe, argv, stderr
from time       import sleep

conf = read_config()


def machine_help():
    parser = ArgumentParser(description='Proxmox Home Cloud remote manager', add_help=False, prog=_getframe().f_code.co_name.replace('_', ' '))
    parser.add_argument('sub', choices=['create', 'delete'], )
    args, unknown = parser.parse_args()

    parser.print_help(stderr)





def machine_delete():
    parser = ArgumentParser(description='Proxmox Home Cloud remote manager', prog=_getframe().f_code.co_name.replace('_', ' '))
    parser.add_argument("--ip", type=str, default="0.0.0.0", help="IP for the VM to use")
    parser.add_argument("--node", type=str, default="pve", help="Node for the VM to use")
    parser.add_argument("--source", type=int, default=9999, help="Node for the VM to use")
    parser.add_argument("--target", type=int, help="Node for the VM to use")
    args, unknown = parser.parse_known_args()

    __pmx = proxmox(conf, node=args.node)
    __ipam = ipam(conf)
    __dns = dns(conf)
    __ca = ca(conf)
    __vm = machine(conf, node=args.node)

    __vm.name = argv[1]

    disk = (__ipam.get_vm_disk_id(__vm.name))
    interface = (__ipam.get_vm_interface_id(__vm.name))
    __id = __pmx.get_vm_id(__vm.name)
    __vm.id = (__id['data'])
    ipam_vm = __ipam.get_vm_id(__vm.name)
    __ip = __pmx.get_vm_ip(__vm.id)
    __vm.ip = (__ip['data'])
    ret = __vm.stop()

    try:
        count = 0
        while __vm.get_status()['data']['data']['status'] != "stopped":
            sleep(1)
            if count > 59:
                return ({'status': False, 'data': "Failed to delete VM (not stopped)"})
            count += 1

        ret = __pmx.delete(__vm.id)
        __status = "deleted"
    except:
        __status = __vm.get_status()['data']['data']['status']
        raise

    vm_ret = (__ipam.delete_vm(ipam_vm['data']))
    record = (__dns.remove_record(__vm.name))
    ca_ret = (__ca.delete_ca(__vm.name))

    sjprint((__vm.name, args.node, "Virtual", __vm.ip, f"{__vm.name}.{conf["network"]["domain"]}", __status))


def machine_create():
    parser = ArgumentParser(description='Proxmox Home Cloud remote manager', prog=_getframe().f_code.co_name.replace('_', ' '))
    parser.add_argument("--ip", type=str, default="0.0.0.0", help="IP for the VM to use")
    parser.add_argument("--node", type=str, default="pve", help="Node for the VM to use")
    parser.add_argument("--source", type=int, default=19999, help="Node ID for the VM to use as source")
    parser.add_argument("--target", type=int, help="Node ID for the VM to use as target")
    args, unknown = parser.parse_known_args()

    __pmx = proxmox(conf, node=args.node)
    __ipam = ipam(conf)
    __dns = dns(conf)
    __ca = ca(conf)
    __vm = machine(conf, args.node)

    __vm.name = argv[1]
    __vm.id = args.target if args.target else __pmx.next_available_id()
    __vm.ip = __ipam.next_available_ip()['data']
    __vm.ip = args.ip if args.ip != "0.0.0.0" else __ipam.next_available_ip()['data']

    ret = __pmx.clone(name=__vm.name, source=args.source, target=__vm.id, full_clone=True)
    if not ret['status']:
        print(f'[PROXMOX] Virtual Machine Cloning   | {ret['data']}')

    ret = __vm.update_ip()
    ret = __vm.start()
    ipam_vm = __ipam.create_virtual_machine(__vm.name)
    ipam_interface = __ipam.create_interface('eth0', ipam_vm['data'])
    ipam_disk = __ipam.create_disk('/', 20, ipam_vm['data'])
    ipam_ip = __ipam.create_ip_address(__vm.name, __vm.ip, ipam_interface['data'])
    ip2vm = __ipam.attach_ip_address_to_virtual_machine(__vm.ip, ipam_vm['data'])
    record = __dns.create_record(__vm.name, __vm.ip_pdns)
    ca_ret = __ca.create_ca(__vm.name)

    sjprint((__vm.name, args.node, "Virtual", __vm.ip, f"{__vm.name}.{conf["network"]["domain"]}", __vm.get_status()['data']['data']['status']))