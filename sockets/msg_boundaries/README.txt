In these examples, we see the difference of message boundary behavior.

TCP gets no packets, just a stream of bytes. So it will relieably get all the bytes the client sends,
but (possibly) in different chunks. When I run the tcp server and client pair, the server picks prints
only two lines wherein, in two recv() calls, it receives all the bytes of three messages.

For UDP on the other hand, packets are packets, and will be read as a whole by recvfrom(). I will
always print three "received" lines on server because client sends three packets. 

Note that I can also make udp drop bytes by making the read buffer smaller than a message that the 
client may send. Then the next read will read the next packet only, and all bytes from the previous
packet that were beyond the buffer are forever lost.
