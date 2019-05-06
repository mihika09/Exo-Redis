import pprint
import bisect

DB = {}
SORTED_SETS = {}


def set_evaluator(command):
	if len(command) != 2:
		return None

	DB[command[0]] = command[1]
	return "+OK\r\n"


def get_evaluator(command):
	if len(command) != 1:
		return None

	key = command[0]
	if key in SORTED_SETS:
		return None

	if key in DB:
		value = DB[key]
		return "${}\r\n{}\r\n".format(len(value), value)

	return "$-1\r\n"


def setbit_evaluator(command):
	if len(command) != 3:
		return None

	try:
		key, offset, cmd_value = command
		offset = int(offset)
		cmd_value = int(cmd_value)
		if cmd_value not in (0, 1):
			return None

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

			offset = (d + l - 1) - offset

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

		return ':{}\r\n'.format(ret)


	except:
		return None


def getbit_evaluator(command):

	if len(command) != 2:
		return None

	key = command[0]

	if key in DB:
		val = DB[key]

		# https://stackoverflow.com/questions/699866/python-int-to-binary-string
		value = ''.join(format(ord(x), '08b') for x in val)

		offset = command[1]
		l = len(value) - 1
		if int(offset) <= l:
			offset = l - int(offset)
			if int(value, 2) & (1 << offset):
				return ':1\r\n'

	return ':0\r\n'


def zadd_evaluator(command):
	if len(command) != 3:
		return None

	key = command[0]
	try:
		score = int(command[1])
	except:
		return None

	element_name = command[2]

	print("Key: {}, Score: {}, Element_name: {}".format(key, score, element_name))

	if key not in DB:
		DB[key] = {element_name: score}
		SORTED_SETS[key] = {score: [element_name]}
		response = ":1\r\n"

	else:
		if key not in SORTED_SETS:
			return None

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

			response = ":0\r\n"

		else:
			DB[key][element_name] = score
			if score in SORTED_SETS[key]:
				bisect.insort(SORTED_SETS[key][score], element_name)
				# SORTED_SETS[key][score].append(element_name)
			else:
				SORTED_SETS[key][score] = [element_name]

			response = ":1\r\n"

	print("DB")
	pprint.pprint(DB)
	print("SORTED_SETS")
	pprint.pprint(SORTED_SETS)

	return response


def zcard_evaluator(command):
	if len(command) != 1:
		return None

	key = command[0]

	if key not in SORTED_SETS:
		return None

	n = len(DB[key])
	return ":{}\r\n".format(n)


def zcount_evaluator(command):
	if len(command) != 3:
		return None

	key, min, max = command

	if key not in SORTED_SETS:
		return None

	try:
		min = int(min)
		max = int(max)
		count = 0

		for i in DB[key]:
			score = DB[key][i]
			if min <= score <= max:
				count += 1

		return ":{}\r\n".format(count)

	except:
		return None


def zrange_evaluator():
	pass


def commands_eval(data):
	evaluators = {"SET": set_evaluator, "GET": get_evaluator, "SETBIT": setbit_evaluator, "GETBIT": getbit_evaluator,
				  "ZADD": zadd_evaluator, "ZCARD": zcard_evaluator, "ZCOUNT": zcount_evaluator, "ZRANGE": zrange_evaluator}

	if data[0] in evaluators:
		evaluated_output = evaluators[data[0]](data[1:])
		if evaluated_output is not None:
			return evaluated_output
		else:
			return "-ERR Invalid Command\r\n"

	return "-ERR Unsupported Command\r\n"
