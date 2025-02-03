import socket
import signal
import sys

# This api call isn't really that "close to the metal". By specifying SOCK_STREAM,
# I'm getting TCP. And I'm getting a "server socket" with this, which will helpfully
# manage and coordinate lots of requests from multiple clients which may be happening
# all at once, but which it will sort into different client sockets for me to read from.

# If it were UDP, there would just be one socket, this one, to call recv/send on.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
active_connections = set()

# Do a little signal handling to be sure to close all connections. Could treat this
# (single-threaded) server as having one global client connection, but this (set) is
# how I'd handle a multi-threaded server.
def cleanup_connections():
    for c in active_connections:
        print("Closing client conn in signal handler")
        c.close() # client connection
    s.close() # server
    sys.exit(0)

def signal_handler(sig, _):
    print("Handling sigint")
    cleanup_connections()

signal.signal(signal.SIGINT, signal_handler)

"""
Prints:
my_socket=<socket.socket fd=3, family=2, type=1, proto=0, laddr=('0.0.0.0', 0)>

fd=3 means file descriptor 3. in unix, "everything is a file"
"""
print(f"{s=}")

try:
    s.bind(('localhost', 8080))

    # listen doesn't block.
    s.listen()
    print("Listening...")
    # Loop over multiple connections
    term_str = 'lmao'
    conn = None
    while True:
        try:
            print("Waiting for new connection")

            conn, client_addr = s.accept() # accept blocks while waiting for connection

            # A connection gotten this way is just another socket. The actual data from and to the client happens not at all
            # through the socket `s` - that's the server socket. It happens only through the conn socket. If I already have
            # a connection being processed and a second client tries to connect to port 8080, the server socket will essentially
            # tell that second client "yes we're open for business" but it will wait until my program is ready to accept a new
            # connection before giving any of the data from that client to the program. This way data doesn't bleed between
            # client connections. Client 2 can be sending data which is isolated from the data sent by client 1 because it's
            # going to be read from a different socket.
            active_connections.add(conn)
            print("Accepted new connection") # Note: as soon as I run `nc localhost 8080`, the connection is created/accepted.

            # recv() blocks, returns as soon as it has any bytes to give, and thus may return incomplete
            # message due to network timing, perhaps

            # The following is the Literal Multiple Action Ontology (L.M.A.O) protocol: all messages
            # are terminated by the string "lmao"

            # loop over receiving data from one connection
            new_data = conn.recv(1024).decode()
            data = new_data
            term_pos = new_data.find(term_str)
            print(f"SERVER: Start read: new_data=[{new_data}], term_pos={term_pos}")
            while (str(new_data) and term_pos == -1):
                new_data = conn.recv(1024).decode()
                data += new_data
                term_pos = data.find(term_str)
                print(f"SERVER: (end loop) read: new_data=[{new_data}], term_pos={term_pos}")
            
            # case where client closed connection without laughter.
            if not new_data:
                print("SERVER: Received incomplete message (not LMAO-compatible)")
                continue # should still close connection in finally block
            data = data[:term_pos] # omit bytes after terminal string
            print(f"SERVER: Received message: data=[{data}]")


            # LMAO protocol supports shutting down the server by way of a client message.
            if "terminate_server" in data:
                break
            conn.send(bytes("That sounds great!\nlmao", 'utf-8'))
        finally:
            # finish processing connection, move on to handle another
            if conn:
                print("Closing connection")
                active_connections.remove(conn)
                conn.close() 
finally:
    print("Closing socket")
    s.close()
