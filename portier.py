from time import sleep
import asyncio
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.1", 54321)
sock.connect(server_address)

sock.sendall("door_state".encode('utf-8'))
print(sock.recv(255).decode('utf-8'))
sock.close()
