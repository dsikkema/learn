```bash

# I have no containers running
 $ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

# But I have other containers that are not running:
 $ docker ps -a
CONTAINER ID   IMAGE                         COMMAND                  CREATED       STATUS                     PORTS                    NAMES
881b6d70d80c   ubuntu:latest                 "/bin/bash"              6 days ago    Exited (255) 5 days ago                             linux
6ba2288a2687   postgres                      "docker-entrypoint.s…"   3 weeks ago   Exited (255) 5 days ago    0.0.0.0:5432->5432/tcp   dvd_rentals_pg
...

# all are exited. Some have exit codes as above like 255, others 0, 137, 1.

# show locally cached images:
 $ docker images
REPOSITORY                  TAG       IMAGE ID       CREATED         SIZE
confluentinc/cp-kafka       latest    adc392d28a1e   2 months ago    1.74GB
confluentinc/cp-zookeeper   latest    5ca5f3269814   2 months ago    1.74GB
nginx                       latest    42e917aaa1b5   2 months ago    280MB
postgres                    latest    87ec5e0a167d   3 months ago    634MB
postgres                    16        c965017e1d29   3 months ago    631MB
postgres                    14        922d38d4ca73   3 months ago    617MB
ubuntu                      latest    80dd3c3b9c6c   3 months ago    139MB
apache/kafka                latest    fbc7d7c428e3   3 months ago    634MB
confluentinc/cp-kafka       7.5.0     fbbb6fa11b25   18 months ago   1.35GB

# a container is essentially an instance of an image

# when a container exists, its filesystem state is preserved - any files created/modified remain intact

# start existing, stopped container from above:
docker start linux # could also use container id, docker start 881b6d70d80c

# because COMMAND is /bin/bash, it stays running
 $ docker ps
CONTAINER ID   IMAGE           COMMAND       CREATED      STATUS         PORTS     NAMES
881b6d70d80c   ubuntu:latest   "/bin/bash"   6 days ago   Up 4 seconds             linux

# ssh into it. Exec "executes a command inside running container"
 $ docker exec -it linux bash

root@881b6d70d80c:/#

# and now, there are two bash processes: PID 1 is the main process or entrypoint process, /bin/bash,
# and I have a separate bash session open.
root@881b6d70d80c:/# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   4300  3504 pts/0    Ss+  17:12   0:00 /bin/bash
root        17  0.0  0.0   4300  3504 pts/1    Ss   17:14   0:00 bash
root        25  0.0  0.0   7632  3148 pts/1    R+   17:14   0:00 ps aux


```
