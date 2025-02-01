import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
my_socket=<socket.socket fd=3, family=2, type=1, proto=0, laddr=('0.0.0.0', 0)>

fd=3 means file descriptor 3. in unix, "everything is a file"
"""
print(f"{my_socket=}")

my_socket.bind(('localhost', 8080))

"""
After bind: my_socket=<socket.socket fd=3, family=2, type=1, proto=0, laddr=('127.0.0.1', 8080)>
"""
print(f"After bind: {my_socket=}")