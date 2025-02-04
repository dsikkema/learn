import socket

for i in range(150):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8080))
    s.send(f"msg={i}".encode())
    s.close()
