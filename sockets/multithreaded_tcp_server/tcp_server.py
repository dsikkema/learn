import socket
import signal
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# this is so once the program exits, the port is immediately freed
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
active_connections = set()

def cleanup_connections():
    # If I were a grown-up I would use thread safe synchronized connection managers or something.
    # 
    # copying the set to avoid race condition where set is mutated while iterating. In this 
    # implementation, I may call close() twice on some connections (the conneciton handler itself may 
    # close one before the signal handler does)
    for c in set(active_connections):
        print("Closing client conn in signal handler")
        c.close() # client connection
    s.close() # server
    sys.exit(0)

def signal_handler(sig, _):
    print("Handling sigint")
    cleanup_connections()

signal.signal(signal.SIGINT, signal_handler)

def hande_connection(conn: socket.socket):
    try:
        sleep(0.75) # simulate long-running work
        thread_id=threading.get_native_id()
        print(f"SERVER:\tHandle connection, thread={thread_id}")
        active_connections.add(conn)
        data = conn.recv(1024)
        msg = data
        while data:
            data = conn.recv(1024)
            msg += data
        print(f"SERVER: Read: {msg.decode()} thread={thread_id}")
    finally:
        conn.close()
        active_connections.remove(conn)

pool = ThreadPoolExecutor(max_workers=4)

try:
    s.bind(('localhost', 8080))
    s.listen()
    while True:
        try:
            print("Waiting for new connection")
            conn, client_addr = s.accept() # accept blocks while waiting for connection

            # submit() returns a future which offers some interesting methods,
            # but I don't need any of them in this implementation
            pool.submit(hande_connection, conn)
        finally:
            pass
finally:
    print("Closing server socket")
    s.close()
