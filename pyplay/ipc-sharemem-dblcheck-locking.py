from multiprocessing import Process, Value, Lock
from typing import Callable
from time import sleep
from random import random
from os import getpid


def incr_ctr_with_race_cond(ctr: Value) -> None:
    while ctr.value < 15:
        sleep(random() / 10)
        print(f"{getpid()=}, doing increment")
        ctr.value += 1
        sleep(random() / 10)  # random in [0,1)


def inc_ctr_broken_lock(ctr: Value, lock: Lock) -> None:
    while ctr.value < 15:
        sleep(random() / 10) # who knows, it could take time to get from one line to the next
        with lock:
            print(f"{getpid()=}, doing increment")
            ctr.value += 1
            sleep(random() / 10)  # random in [0,1)

def incr_ctr_doublecheck_lock(ctr: Value, lock: Lock) -> None:
    while ctr.value < 15:
        sleep(random() / 10) # who knows, it could take time to get from one line to the next
        with lock:
            if ctr.value >= 15:
                break
            print(f"{getpid()=}, doing increment")
            ctr.value += 1
            sleep(random() / 10)  # random in [0,1)

def try_race_cond():
    print("\n\nTry naively. This MAY produce race condition and > 15 value. \n\n")
    shared_ctr = Value("i", 0)
    processes = [
        Process(target=incr_ctr_with_race_cond, args=[shared_ctr]) for _ in range(3)
    ]
    for p in processes:
        p.start()

    while shared_ctr.value < 15:
        print(f"{shared_ctr.value=}")
        sleep(0.1)

    for p in processes:
        p.join()

    print(f"Final value: {shared_ctr.value=}")

def try_with_lock(inc_ctr_fn: Callable[[Value, Lock], None]):
    print("\n\nTry with locking. Does it work or produce race condition? Depends on locking strategy... \n\n")
    print(f"{inc_ctr_fn=}")
    shared_ctr = Value("i", 0)
    shared_lock = Lock()
    processes = [
        # use callback given as parameter
        Process(target=inc_ctr_fn, args=[shared_ctr, shared_lock]) for _ in range(3)
    ]
    for p in processes:
        p.start()

    while shared_ctr.value < 15:
        print(f"{shared_ctr.value=}")
        sleep(0.1)

    for p in processes:
        p.join()

    print(f"Final value: {shared_ctr.value=}")


if __name__ == "__main__":
    try_race_cond()
    try_with_lock(inc_ctr_broken_lock)
    try_with_lock(incr_ctr_doublecheck_lock)


