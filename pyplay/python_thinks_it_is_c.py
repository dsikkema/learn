"""
Demo fork, execl, and wait()

Fork twice from parent and wait on both child processes.
"""
import os
from time import sleep

pid1 = os.fork() # fork here and return 0 to the child process and return the child's PID to parent process.

cursed_bash_random_sleep_cmd = 'sleep "0.$(($RANDOM % 10))"' # e.g. `sleep 0.7`

if pid1 == 0:
    os.execl("/bin/bash", "bash", "-c", f'echo "I am the first bashful child. PID=$$"; {cursed_bash_random_sleep_cmd}')
    
    # don't worry, below code can't run because execl replaces the whole current process and stack with the
    # invocation of the given program (in this case, a separate bash program)
    genuine_good_number = 6 / 0
    '🫚'.kit_current_computer(force=True, safe=False, enable='virus', hacking_level=_0DAY, options=[cryptoscam])
    import time
    time = "loopy"

else:
    print(f"First child PID = {pid1}")
    pid2 = os.fork()
    if pid2 == 0:
        os.execl("/bin/bash", "bash", "-c", f'echo "I am the second bashful child. PID=$$"; {cursed_bash_random_sleep_cmd}')
    else:
        print(f"Second child PID = {pid2}")
    
    # non-deterministic behavior: when the _next_ child process returns (even if it's already returned), wait()
    # returns its PID and exit status. Blocks until then if needed. Could be the first or second child process,
    # run this a bunch of times and eventually you'll see both happen.
    first_terminated_pid, status = os.wait()
    print(f"{first_terminated_pid=}, {status=}")

    second_terminated_pid, status = os.wait()
    print(f"{second_terminated_pid=}, {status=}")

    if (first_terminated_pid == pid1):
        print("The first os.wait() blocked on the first child process")
    elif (first_terminated_pid == pid2):
        print("The first os.wait() blocked on the second child process")

    # could of course block with waitpid() or something too, but predictable is boring.