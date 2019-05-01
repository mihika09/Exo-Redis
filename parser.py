DB = {}


async def read_command(reader):

	data = await reader.readuntil(b'\r\n')
	data = data.decode()
	if data[0] != '$':
		raise Exception('Invalid command')

	b = int(data[1])
	arg = await reader.readexactly(b + 2)
	return arg.decode().split()[0]


async def getbit_parser(reader, n):

	if n != 2:
		raise Exception('Invalid Command')

	key = await read_command(reader)

	if key in DB:
		val = DB[key]

		# https://stackoverflow.com/questions/699866/python-int-to-binary-string
		value = ''.join(format(ord(x), '08b') for x in val)

		offset = await read_command(reader)
		l = len(value) - 1
		if int(offset) <= l:
			offset = l - int(offset)
			if int(value, 2) & (1 << offset):
				return ':1\r\n'

		return ':0\r\n'


async def set_parser(reader, n):

	if n != 2:
		raise Exception('Invalid Command')

	key = await read_command(reader)
	value = await read_command(reader)

	DB[key] = value
	print("DB: ", DB)


async def get_parser(reader, n):
	if n != 1:
		raise Exception('Invalid command')

	key = await read_command(reader)
	if key in DB:
		value = DB[key]
		return "${}\r\n{}\r\n".format(len(value), value)
	else:
		return "$-1\r\n"


async def command_parser(reader, n):

	"""can use a dict to map the command (key) to the function (value)"""

	try:
		n = int(n)

		redcom = await read_command(reader)
		n -= 1

		if redcom == 'SET':
			await set_parser(reader, n)
			return "+OK\r\n"

		elif redcom == 'GET':
			response = await get_parser(reader, n)
			return response

		elif redcom == 'GETBIT':
			response = await getbit_parser(reader, n)
			return response

		else:
			return ':0\r\n'

	except:
		return "-ERR Invalid Command\r\n"
