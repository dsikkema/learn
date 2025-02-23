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

# now exit the container. run a new container. running actually does three things:
# pull (an image), create (a container) and start (that container). Those three
# are all also their own docker cmds. In this example, "ubuntu:latest" is the name
# and version of the image, "ubuntu-test" is the name of the container.

 $ docker run --name ubuntu-test ubuntu:latest date
Sun Feb 23 04:15:50 UTC 2025

# it runs and immediately exits. 

# docker start won't automatically connect to the output of the container, though
 $ docker start ubuntu-test
 $ # (prints nothing)

# but --interactive attach

# how does docker start know which command to run inside the container? It's baked into container definition.
# see COMMAND in ps output: an entry point and arguments to it are part of the container. E.g. this line:
 $ docker ps -a | awk '(NR==1 || /postgres:16/) {print $0}'
CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS                     PORTS                    NAMES
f7eb36498aa6   postgres:16                   "docker-entrypoint.s…"   5 weeks ago     Exited (255) 4 weeks ago   0.0.0.0:5432->5432/tcp   twitter-clone-db

# entrypoint is some dedicated script inside the container which obviously starts the (long-running) docker server process.

# can also see that information with docker inspect. Entrypoint and Cmd are basically concatenated as the command that gets run, `docker-entrypoint.sh postgres`.

 $ docker inspect twitter-clone-db | jq '.[0].Config.Cmd, .[0].Config.Entrypoint'
[
  "postgres"
]
[
  "docker-entrypoint.sh"
]

# now what about this enigma?
$ docker start ubuntu-test
$ 
# (no output)

# well, "run" captures output by default. start doesn't. So need to use
# interactive mode for start.
$ docker start -i ubuntu-test 
$ #( should print date now)

# what if you want to be able to get into a bash shell inside that container?

# It cannot really be done, unless you happen to launch 
# `docker exec -it ubuntu-test bash` at the exact moment during which the
# container is running (running the `date` command) and hasn't exited 
# yet - almost impossible unless (maybe) you have a background script 
# constantly and in parallel starting the container in loop, and try to 
# exec in enough times, but that's gross

# Yeah that is gross, I want to change the entry point to bash

# You can't do that.

# Sure I can, tell me how.

# No, you can't. It's not how docker is meant to be used.

# I have a sharp stick and a case of red bull telling me that I don't much
# care how docker is meant to be used.

$ docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh
# (inside VM that runs the docker daemon on macos)

# dir for container in question
cd /var/lib/docker/containers/3fc3fb1646acb3745e44c6c5ffd402e4386eee9abdbc3ef4bf0270264454b7e6/

# change configuration of the container, change the Command from date to bash, and enable a bunch of std and tty related things
sed -i 's/date/bash/g' config.vs.json
sed -i -e 's/"AttachStdin":false/"AttachStdin":true/' -e 's/"OpenStdin":false/"OpenStdin":true/' -e 's/"Tty":false/"Tty":true/' -e 's/"StdinOnce":false/"StdinOnce":true/' config.v2.json

# then restart docker, and...
 $ docker start -i ubuntu-test
root@3fc3fb1646ac:/# echo "Resplendent glory abides."
Resplendent glory abides.

# don't live life the way docker wants you to live it. Make docker live the way YOU want to live.
```
