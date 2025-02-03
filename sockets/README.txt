For dealing with the TCP example (py_socket.py)

`nc localhost 8080`.

Can have multiple of these open in multiple terminals, each sending data simultaneously, and 
the requests will be handled serially by the single-threaded server (but treated as different
requests).

localhost can resolve because it's TCP.

For UDP:

`nc -u 128.0.0.1 8080`. -u for UDP (TCP is default). Somehow the process here, being more 
barebones, doesn't allow for a negotiation process to let "localhost" resolve to something 
else.

And this one, multiple connections open at once in different terminals, will all print lines/bytes 
to server output at the time time.

