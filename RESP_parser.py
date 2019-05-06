def string_parser(data):
	if data[0][0] != '+':
		return None

	return data[0][1:]


def integer_parser(data):
	if data[0][0] != ':':
		return None

	try:
		n = int(data[0][1:])
		return n

	except:
		return None


def bulk_string_parser(data):

	if data[0][0] != '$':
		return None

	try:
		n = int(data[0][1:])

		# Null element
		if n == -1:
			return "None"

		if data[1] != data[1][0:n]:
			return None

		return data[1], data[2:]

	except:
		return None


def array_parser(data):

	res = []
	if data[0][0] != '*':
		return None

	try:
		n = int(data[0][1:])
		i = 1
		data = data[1:]
		while i <= n:
			value, data = parsers(data)
			if value is None:
				return None

			res.append(value)
			i += 1

		return res, data

	except:
		return None


def parsers(data):

	parsers = [bulk_string_parser, array_parser]
	for parser in parsers:
		result = parser(data)
		if result is not None:
			res, data = result
			# print("res: ", res, "data: ", data)
			return res, data

	return None


def RESP_parser(data):
	data = data.split('\r\n')
	response, data = parsers(data)
	if data == ['']:
		return response
	return None
