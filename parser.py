DB = {}


async def read_command(reader):

	data = await reader.readuntil(b'\r\n')
	data = data.decode()
	if data[0] != '$':
		raise Exception('Invalid command')

	b = int(data[1])
	arg = await reader.readexactly(b + 2)
	return arg.decode().split()[0]


async def set_parser(reader, n):

	if n != 2:
		raise Exception('Invalid command')

	key = await read_command(reader)
	value = await read_command(reader)

	print("Key: ", key)
	print("Value: ", value)

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

	try:
		n = int(n)
		print("array n: ", n)

		redcom = await read_command(reader)
		n -= 1

		if redcom == 'SET':
			await set_parser(reader, n)
			return "+OK\r\n"

		elif redcom == 'GET':
			response = await get_parser(reader, n)
			return response


	except:
		return "-ERR Invalid Command\r\n"
