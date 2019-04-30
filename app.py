import asyncio

HOST = "127.0.0.1"
PORT = 15000


async def exo_redis(reader, writer):
	while True:
		data = await reader.read(1024)
		if not data:
			break;
		print("Data: ", data)
		response = "+OK\r\n"
		print("response: ", response)
		writer.write(response.encode())
		await writer.drain()

	writer.close()



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
