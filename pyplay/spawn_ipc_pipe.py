"""
Use a spawned process (the default for starting processes with multiprocessing module) to receive data from parent.
Don't need to be as fussy about closing the write end of the pipe: due to the process being spawned, not forked, it
doesn't inherit file descriptors from the parent process, hence `os.pipe()` doesn't work (at least not smoothly) to
create a 1-way pipe that actually connects the two processes. `multiprocessing.Pipe` takes care of that and also
obviates the need to close the write end from the pipe reader.
"""
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection

def child_proc_fork(conn: Connection):
    print("Child begun")

    while True:
        try:
            msg = conn.recv()
            print(f"Child read: {msg=}")
        except EOFError:
            # the standard way to handle end of input. Exception means nothing to receive AND other end closed.
            break

    print("Child finished")
    conn.close()

def main():
    print("Main begun")
    child_conn, parent_conn = Pipe()

    child = Process(target=child_proc_fork, args=[child_conn])
    child.start()

    for line in ['You', 'cannot', 'pass']:
        parent_conn.send(line)
    parent_conn.close()

    child.join()

if __name__ == "__main__":
    main() 