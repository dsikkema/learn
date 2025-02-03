# TCP
tcp_socket.py


`nc localhost 8080`.

Can have multiple of these open in multiple terminals, each sending data simultaneously, and 
the requests will be handled serially by the single-threaded server (but treated as different
requests).

localhost can resolve because it's TCP.

Can also send a curl request. The whole HTTP headers etc will print out. E.g. `curl localhost:8080 -d 'haha lmao'`
will cause the following to be logged:

```
Accepted new connection
SERVER: Start read: new_data=[POST / HTTP/1.1
Host: localhost:8080
User-Agent: curl/8.7.1
Accept: */*
Content-Length: 9
Content-Type: application/x-www-form-urlencoded

haha lmao], term_pos=151
SERVER: Received message: data=[POST / HTTP/1.1
Host: localhost:8080
User-Agent: curl/8.7.1
Accept: */*
Content-Length: 9
Content-Type: application/x-www-form-urlencoded

haha ]
Closing connection
```

Note how, because the "body" of the post request comes last, as long I put "lmao" in the body, it will successfully
read in the TCP server's processing as a message termination.

The most interesting thing this shows is just how HTTP is really visible and legible as a stream of ascii bytes, even on the lowest socket layers.

The server will of course send a non-http response and curl will by default fail on that, but that's to be expected.

For UDP:

`nc -u 128.0.0.1 8080`. -u for UDP (TCP is default). Somehow the process here, being more 
barebones, doesn't allow for a negotiation process to let "localhost" resolve to something 
else.

And this one, multiple connections open at once in different terminals, will all print lines/bytes 
to server output at the time time.

