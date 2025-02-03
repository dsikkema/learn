import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8080))

long_msg = """
To me, fair friend, you never can be old,
For as you were when first your eye I eyed,
Such seems your beauty still. Three winters cold
Have from the forests shook three summers' pride,
Three beauteous springs to yellow autumn turn'd 
In process of the seasons have I seen,
Three April perfumes in three hot Junes burn'd,
Since first I saw you fresh, which yet are green.
"""
s.send(f"First msg: {long_msg}".encode())
s.send(f"Second msg: {long_msg}".encode())
s.send(f"Third msg: {long_msg}".encode())