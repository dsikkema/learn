from multiprocessing import Process
from time import time

"""
Demonstrate process blocking/suspension behavior.

In theory, "spinning" should be a good bit slower than using join() to wait for child processes, and slower than just
doing all the (sequential and not parallel) computation in one process.

In reality, the CPU scheduler seems to have great heuristics about recognizing the spinning - that a thread keeps
waiting for a certain result and not getting it, and it deprioritizes the spining thread, leading to pretty similar
results (a little slower in both multiprocessing cases, but not "double as slow" as you might expect if the scheduler
was wasting a large share of the possible cpu cycles on the parent process.

 # sample result
 $ python multiprocess_suspension.py
Single process: elapsed=2.702. Per job = 0.676
Sequential multiprocess (spin): elapsed=2.769, Per job = 0.692
Sequential multiprocess (join): elapsed=2.783, Per job = 0.696
"""

def long_f():
    x = 0
    for i in range(1, 10000000):
        x = i**2 / i**(0.2342)

def main():
    # Result with no child processes
    n_jobs = 4
    tic=time()
    for _ in range(n_jobs):
        long_f()
    toc = time()
    elapsed=toc-tic

    print(f"Single process: {elapsed=:.3f}. Per job = {elapsed / n_jobs:.3f}")

    # Child processes, in sequence, "wait" for them by spinning
    processes = []
    for _ in range(n_jobs):
        p = Process(target=long_f)
        processes.append(p)
    
    """
    Intentionally doing this BADLY. This runs each process not in parallel but
    in sequence in order to get a sense of how much overhead is involved, and
    how much time _both between the parent and the child process_ is, on average,
    spent doing the job.
    """
    tic = time()
    checks = []
    for p in processes:
        p.start()
        c = p.is_alive()
        while c:
            checks.append(c)
            c = p.is_alive()
    toc = time()
    elapsed = toc-tic

    print(f"Sequential multiprocess (spin): {elapsed=:.3f}, Per job = {elapsed / n_jobs:.3f}")


    # Child processes, in sequence, use join() to block waiting for them
    processes = []
    for _ in range(n_jobs):
        p = Process(target=long_f)
        processes.append(p)
    tic = time()
    for p in processes:
        p.start()
        p.join()
    toc = time()
    elapsed = toc-tic

    print(f"Sequential multiprocess (join): {elapsed=:.3f}, Per job = {elapsed / n_jobs:.3f}")
if __name__ == "__main__":
    main()
