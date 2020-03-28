import socket
import netifaces as ni

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

server_host = "0.0.0.0"
port = 8080

s.bind((server_host, port))
s.listen(10)
print(f"[*] Listening as {server_host}:{port}")

client_socket, address = s.accept()

print(f"[+] {address} is connected.")
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

client_socket.close()
print("[x] Closed client socket.")
s.close()
print("[x] Closed main socket.")
