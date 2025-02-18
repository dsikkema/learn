```
[ ~/home/learn/c/linux_c (main) ]
 $ docker start linux
linux
[ ~/home/learn/c/linux_c (main) ]
 $ docker exec linux /code/target/hello
Hello, world
```

For `fork_exec` (syscall is not deprecated on linux the way it is on mac):
```
 $ docker exec linux bash -c "cd /code && gcc fork_exec.c -o target/fork_exec && target/fork_exec"
total 12
-rw-r--r-- 1 root root  157 Feb 16 09:59 README.md
-rw-r--r-- 1 root root 1017 Feb 16 09:59 fork_exec.c
-rw-r--r-- 1 root root   65 Feb 16 09:51 hello.c
drwxr-xr-x 4 root root  128 Feb 16 10:00 target

Demoing fork:

Parent: pid=43, child_pid=53
Child process finished, status=0

Demo syscall:

PIDs: direct syscall = 43, lib = 43%        
```
