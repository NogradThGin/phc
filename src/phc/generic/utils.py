from .errors import OutputSizeMismatch

def jprint(content:list, justifier:int=20):
	__justifier = r'{:<' + str(justifier) + r'}'
	__format = str()

	for count in range(0, len(content)):
		__format += f"{__justifier} "
	__format = __format[:-1]

	print(__format.format(*content))

def sjprint(content:list, header:list=("NAME", "NODE", "MACHINE_TYPE", "INTERNAL_IP", "DNS", "STATUS"), justifier:int=20):
	__justifier = r'{:<' + str(justifier) + r'}'
	__format = str()

	if len(content) != len(header):
		raise OutputSizeMismatch("Header and content have inconsistent size")

	for count in range(0, len(content)):
		__format += f"{__justifier} "
	__format = __format[:-1]

	print(__format.format(*header))
	print(__format.format(*content))