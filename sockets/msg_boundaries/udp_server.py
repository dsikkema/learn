import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost', 8080))
while True:
    data, _ = s.recvfrom(1024)
    print(f"SERVER:\tReceived. msg=[{data.decode()}]")
