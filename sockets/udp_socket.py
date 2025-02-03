import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM makes it UDP
s.bind(('localhost', 8080))

# UDP gives a "from_addr" in its result because it doesn't guaruntee
# that only one client is communicating on a given socket
#
# Note how I'm receiving directly on the one socket I opened, no
# accept() or listen()
while True:
    data, from_addr = s.recvfrom(1024)
    print(f"Received {data.decode()} from {from_addr}")
print("Finished")
