"""
Use a forked (not spawned, which is default) process to receive data from parent 
using a 1-way pipe for IPC. Must be fussy about closing the writing end of the 
pipe in both processes to guarantee the EOF signal will be sent.

Using a forked process means file descriptors are inherited from parent to child
process and therefore `os.pipe()` can be used - the same file descriptor integers
are "valid" and able to be used in both processes.
"""
import os
from multiprocessing import Process
import multiprocessing

def child_proc_fork(read_fd: int, write_fd: int):
    print("Child begun")

    # writer_fd only used by parent, but needs to be closed both in parent
    # and child proc, otherwise this proc won't get an EOF signal (zero bytes
    # read), and that's because there's still at least 1 process open (child
    # process, if child fails to closer write_fd, or the parent process if parent
    # fails to do so) which, from the OS perspective "might" still write bytes to
    # it. Therefore, never getting EOF signal, the read loop will hang forever.
    
    # EOF signal is only sent when there's nothing to read AND "other end" has closed.
    os.close(write_fd)

    read_end = os.fdopen(read_fd, 'r')
    for line in read_end:
        print(f"Child read: {line=}")
    print("Child finished")

def main():
    print("Main begun")
    read_fd, write_fd = os.pipe()

    child = Process(target=child_proc_fork, args=[read_fd, write_fd])
    child.start()

    write_end = os.fdopen(write_fd, 'w')
    for line in ['You', 'cannot', 'pass']:
        write_end.write(line + "\n")
    write_end.flush()

    # see note in child process about closing the write end. After opening the
    # write_fd as though it were a file (everything is a file), closing that 
    # file object is the same as os.close(write_d)
    write_end.close() # alternately, os.close(write_fd)
    os.close(read_fd) 

    child.join()

if __name__ == "__main__":
    # should only call this once per program.
    # could also do pid=os.fork(), and then in subsequent code child pid to see if running
    # as parent or child. But multiprocessing library supports forking.
    multiprocessing.set_start_method('fork')
    main() 