Docker setup meant to run C and assembly code inside linux, where some things are easier
than in Macos.

Mounts c and assembly dirs into the container so code can be edited on host machine but run in linux.
# Usage
```bash
docker-compose up -d # one time setup
docker start linux_dev # whenever the container is stopped, neet to start before exec-ing into it
docker exec -it linux_dev bash # get into the container
```

# Development Example
```bash
 $ docker exec -it linux_dev bash # from host machine
root@e30b494e8488:/# cd /c # now inside container
root@e30b494e8488:/c# gcc fork_exec.c -o target/fork_exec
root@e30b494e8488:/c# target/fork_exec 

Demoing fork:

Parent: pid=29, child_pid=30
... # remainder of output
```

# Image specs
Creates an image with some added general utilities (tree and vim), dev tools (gcc, gdb, binutils), and 
man page support (gotten by installing and running unminimize then installing various man packages) so
I can use linux man pages inside the container.

The command is `sleep infinity` so that when started with `docker start`, it will have a long-lasting
process to keep it running:
```bash
root@e30b494e8488:/c# ps aux | awk '(NR == 1 || $2 == 1) {print $0}' # awk: print if (is_header OR PID==1)
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   2272  1004 pts/0    Ss+  20:31   0:00 sleep infinity
```

The process with PID=1 is always the docker container's entrypoint process.
