FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -u unminimize && \
    yes | unminimize && \
    apt-get install -y man man-db manpages-posix vim tree gcc gdb binutils less && \
    rm -rf /var/lib/apt/lists/*

CMD ["sleep", "infinity"]

