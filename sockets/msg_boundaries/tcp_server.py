import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 8080))
s.listen()
conn, _ = s.accept()
while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"SERVER:\tReceived. msg=[{data.decode()}]")
