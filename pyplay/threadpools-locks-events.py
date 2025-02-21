from concurrent.futures import ThreadPoolExecutor
import threading
from time import sleep


def g():
    print("I am a g")


# just run thread, no IO
t = threading.Thread(target=g, daemon=True)
t.start()

# thread with IO: to get return value, you either use memory sharing with a pass-by-reference parameter given as a an
# arg to the function (args=[...] param in above example) or use something like ThreadPoolExecutor. Memory sharing is
# fundamentally the only way to get data out of the thread.


def f(x):
    return x**2


with ThreadPoolExecutor() as executor:
    # note different syntax: args, kwargs of "f()" given directly to "submit()"
    future = executor.submit(f, 5)  # f(x) returns x**2
    res = future.result()
    print(res)


class TimeoutException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


# more basic mem sharing
class ThreadOutputHolder:
    def __init__(self, wait_inside_lock: bool):
        self._wait_inside_lock = wait_inside_lock  # demo threadlocking bug
        self._val = None
        # don't allow race condition in case of multiple threads (not using multiple threads in this case)
        self._lock = threading.Lock()
        # allow for blocking on this object until value is ready
        self._has_val = threading.Event()

    def put(self, val):
        with self._lock:
            self._val = val
            self._has_val.set()

    def get(self):
        # Note: if do the waiting _inside_ the lock, there will be a deadlock. Timeline:
        # 0: main thread launches worker
        # 1: main thread almost-instantly calls get() and acquires the lock
        # 2: after sleeping or doing some work for a little bit of time, worker thread tries to acquire the lock
        #    but is unable to because main thread is already holding it while waiting, hence it waits forever to
        #    put the value while main thread waits forever for it to put the value.

        if not self._wait_inside_lock:
            self._has_val.wait(timeout=5)
        with self._lock:
            if self._wait_inside_lock:
                did_timeout = not self._has_val.wait(timeout=1.5) # wait returns False on timeout
                if did_timeout:
                    raise TimeoutException()
            return self._val


def h(x, holder: ThreadOutputHolder):
    print("Entered h. Sleeping...")
    sleep(0.75)
    holder.put(x**2)


# successfully retrieve the value from the thread
holder = ThreadOutputHolder(wait_inside_lock=False)
threading.Thread(target=h, args=[7, holder]).start()
res = holder.get()  # blocks, waiting on the sleepy thread to finish
print(res)

# now timeout due to thread lock
caught_exc: TimeoutException = None
try:
    holder = ThreadOutputHolder(wait_inside_lock=True)
    threading.Thread(target=h, args=[7, holder]).start()
    res = holder.get()
except TimeoutException as te:
    caught_exc = te

assert caught_exc
if caught_exc:
    print(f"The expected exception occured: {type(caught_exc)}")
