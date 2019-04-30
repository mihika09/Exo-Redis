"""import socket

HOST = "127.0.0.1"
PORT = 15000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	conn, addr = s.accept()
	with conn:
		print('Connected by: {}\nSocket object: {}'.format(addr, conn))
		while True:
			data = conn.recv(1024)
			if not data:
				break;
			print("data: ", data.decode())
"""

import asyncio

HOST = "127.0.0.1"
PORT = 15000


async def exo_redis(reader, writer):
	while True:
		data = await reader.read(1024)
		if not data:
			break;
		print("Data: ", data)
		print("String data: ", str(data.decode()))
		writer.write("Yellow!".encode())
		await writer.drain()

	writer.close()


async def main():
	server = await asyncio.start_server(exo_redis, HOST, PORT)
	await server.serve_forever()


asyncio.run(main())
