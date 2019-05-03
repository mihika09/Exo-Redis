import pprint
import bisect

DB = {}
SORTED_SETS = {}


async def read_command(reader):

	data = await reader.readuntil(b'\r\n')
	data = data.decode()
	if data[0] != '$':
		raise Exception('Invalid command')

	b = int(data[1])
	arg = await reader.readexactly(b + 2)
	return arg.decode().split()[0]


async def setbit_parser(reader, n):

	if n != 3:
		raise Exception("Invalid Command")

	key = await read_command(reader)
	offset = await read_command(reader)
	value = await read_command(reader)
	offset = int(offset)
	cmd_value = int(value)
	ret = 10

	if key in DB:
		val = DB[key]
		value = ''.join(format(ord(x), '08b') for x in val)

		l = len(value)
		d = 0
		ret = 10

		if offset >= l:
			d = ((offset // 8) + 1) * 8 - l
			value = value + '0' * d
			ret = 0

		offset = (d+l-1) - offset

		if ret == 10:
			ret = 1 if (int(value, 2) & (1 << offset)) else 0

		if cmd_value == 0:
			value = int(value, 2) & ~(1 << offset)

		else:
			value = int(value, 2) | (1 << offset)

	else:
		d = ((offset // 8) + 1) * 8
		value = '0' * d

		if cmd_value == 1:
			offset = (d - 1) - offset

			value = int(value, 2) | (1 << offset)

		ret = 0

	if value <= 127:
		DB[key] = chr(value)

	else:
		DB[key] = hex(value)

	print("\nDB[key]: {}\n".format(DB[key]))
	return ':{}\r\n'.format(ret)


async def getbit_parser(reader, n):

	"""Test if key is not present"""

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
		if key in SORTED_SETS:
			raise Exception('Invalid command')

		value = DB[key]
		return "${}\r\n{}\r\n".format(len(value), value)
	else:
		return "$-1\r\n"


async def zadd_parser(reader, n):
	if n != 3:
		raise Exception('Invalid command')

	key = await read_command(reader)
	score = await read_command(reader)
	element_name = await read_command(reader)

	print("Key: {}, Score: {}, Element_name: {}".format(key, score, element_name))

	if key not in DB:
		DB[key] = {element_name: score}
		SORTED_SETS[key] = {score: [element_name]}

	else:
		if key not in SORTED_SETS:
			raise Exception('Invalid command')

		if element_name in DB[key]:  # update the score for the element in DB and SORTED_SETS
			old_score = DB[key][element_name]
			if old_score != score:
				DB[key][element_name] = score
				SORTED_SETS[key][old_score].remove(element_name)
				if score in SORTED_SETS[key]:
					bisect.insort(SORTED_SETS[key][score], element_name)
					# SORTED_SETS[key][score].append(element_name)
				else:
					SORTED_SETS[key][score] = [element_name]

		else:
			DB[key][element_name] = score
			if score in SORTED_SETS[key]:
				bisect.insort(SORTED_SETS[key][score], element_name)
				# SORTED_SETS[key][score].append(element_name)
			else:
				SORTED_SETS[key][score] = [element_name]

	print("DB")
	pprint.pprint(DB)
	print("SORTED_SETS")
	pprint.pprint(SORTED_SETS)


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

		elif redcom == 'SETBIT':
			response = await setbit_parser(reader, n)
			return response

		elif redcom == 'ZADD':
			print("***Inside ZADD parser***")
			response = await zadd_parser(reader, n)
			return ":1\r\n"

		else:
			return ':0\r\n'

	except:
		return "-ERR Invalid Command\r\n"
