"""if data[0] == '*':
				response = await command_parser(reader, data[1:])

			else:
			response = "-ERR invalid command\r\n".encode()"""

import asyncio
from parser import command_parser

HOST = "127.0.0.1"
PORT = 15000


async def exo_redis(reader, writer):

	try:
		while True:
			data = await reader.readuntil(b'\r\n')
			if not data:
				break
			print("Data: ", data)
			if data[0] != '*':
				response = await command_parser(reader, data[1:])

			else:
				response = "-ERR invalid command\r\n"
			# response = "+OK\r\n"
			try:
				writer.write(response.encode())
				await writer.drain()

			except ConnectionResetError:
				pass

		writer.close()

	except asyncio.streams.IncompleteReadError:
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
