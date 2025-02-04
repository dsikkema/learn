This tcp_server handles requests in multithreaded fashion with a thread pool of 4 workers.
There is a sleep() in the handle_connection method to simulate long-running tasks.

You can see, when the client rapidly makes 15 connections, the client then exits, while 
(because of delay in handling each connection) the server only processes at max 4 at a 
time, even though it _accepts_ all 15 requests rapidly. All 15 get submitted to the pool,
and the pool lets them sit happily waiting until one of the 4 workers becomes available
to handle it.

Hence there are 4 "spurts" of logs on the server side that handle each batch of (at most) 
4 requests.