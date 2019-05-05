import asyncio
from parser import command_parser

HOST = "127.0.0.1"
PORT = 15000


"""async def exo_redis(reader, writer):
	try:
		while True:
			data = 1
			while data:
				data = await reader.read(n=-1)
				print("data: ", data)

			if not data:
				break

			print("data: ", data)
			response = ":0\r\n"
			print("response: ", response)
			writer.write(response.encode())
			await writer.drain()

		writer.close()

	except:
		pass"""


async def exo_redis(reader, writer):

	try:
		while True:
			data = await reader.readuntil(b'\r\n')
			if not data:
				break
			print("Data: ", data)
			data = data.decode()
			if data[0] == '*':
				response = await command_parser(reader, data[1:])

			else:
				response = "-ERR invalid command\r\n"

			try:
				print("response: ", response)
				writer.write(response.encode('utf-8'))
				await writer.drain()

			except ConnectionResetError:
				print("^_^_^_^_^_^_^_^_^_^")
				pass

		writer.close()

	except asyncio.streams.IncompleteReadError:
		print("*^_^_^_^_^_^_^_^_^_^")
		pass


def start_server():
	loop = asyncio.get_event_loop()
	coro = asyncio.start_server(exo_redis, HOST, PORT)
	server = loop.run_until_complete(coro)
	print("Serving on ", HOST, "port: ", PORT)
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		print("\nShutting Down Server...\n")
	finally:
		server.close()
		loop.run_until_complete(server.wait_closed())
		loop.close()


if __name__ == '__main__':
	start_server()
