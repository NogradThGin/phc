from generic  import read_config, jprint
from objects  import *

from argparse import ArgumentParser
from sys      import _getframe

conf = read_config()


def vms_list():
	parser = ArgumentParser(description='Proxmox Home Cloud remote manager', add_help=False, prog=_getframe().f_code.co_name.replace('_', ' '))
	args, unknown = parser.parse_known_args()

	node="pve"

	jprint(("NAME", "NODE", "MACHINE_TYPE", "INTERNAL_IP", "DNS", "STATUS"))

	__pmx = proxmox(conf, node=node)

	for vm in __pmx.list_vms():
		__vm = machine(conf, node=vm['node'])
		__vm.name = vm['name']
		__vm.id = vm['vmid']
		__status = vm['status']
		try:
			__vm.ip = __pmx.get_vm_ip(__vm.id)['data']
		except:
			print(vm)

		jprint((__vm.name, vm['node'], "Virtual", __vm.ip, f"{__vm.name}.{conf["network"]["domain"]}", __status))

		# __vm.ip = (__ip['data'])

		# sjprint((__vm.name, args.node, "Virtual", __vm.ip, f"{__vm.name}.{conf["network"]["domain"]}", __status))