import asyncio
import aiohttp
import datetime
from time import sleep
from contextlib import AsyncExitStack

print("Section 0: Ctx mgr basic\n\n")
class MyCtxMgr:
    def __enter__(self):
        print("Enter ctx mgr")
        return self
    def __exit__(self, *args, **kwargs): # args are exception type, exception, and traceback
        print("exit ctx mgr")

with MyCtxMgr() as ctx:
    print("I'm in")

print("Section 1: Ctx mgr async\n\n")

class MyAsyncCtxMgr:
    # cannot call await without wrap in async func
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print(f"Enter async ctx mgr, {self.name=}")
        await asyncio.sleep(0.1)
        return self
    async def __aexit__(self, *args, **kwargs):
        print(f"Exit async ctx mgr, {self.name=}")
        await asyncio.sleep(0.1)


# cannot call an asynch ctx mgr without an async invocation
async def f():
    async with MyAsyncCtxMgr("fancy") as ctx:
        print("I'm asynchronously in")

async_ret_val = f()
# async_ret_val=<coroutine object f at 0x104fa9380>, type=<class 'coroutine'>
print(f"{async_ret_val=}, type={type(async_ret_val)}")
print("about to start sleep")
sleep(0.25)
print("finish sleep")

# same as asyncio.run(f())
# only now will the stdout from inside the coroutines be printed.
# before now, the coroutine is created but not run.
asyncio.run(async_ret_val) 

print("Section 2: AsyncExitStack \n\n")

async def g():
    async with AsyncExitStack() as stack:
        # don't need separate with stmts for each one
        db = await stack.enter_async_context(MyAsyncCtxMgr("database"))
        redis = await stack.enter_async_context(MyAsyncCtxMgr("redis"))
        print(f"I'm inside the async exit stack")

asyncio.run(g())

print("Section 3: Parallelism demo with timer\n\n")

"""
The big thing here is to see how the parallelism, enabled by calling potentially
slow things with "await", works even without multiple threads. This is all single-
threaded parallelism. The kernels has a loop that watches for all sorts of OS events
indicating when things become available in order to go back to executing those
tasks. Then API, then, is rather similar to a thread-based futures library, inc-
luding the ability to "gather", that is to say, to create a coroutine that waits
until all the others are finished and returns their results all combined.
"""

async def f1(key: str, use_async_sleep: bool = True):
    print("Inside task: about to sleep 0.5 seconds")
    if use_async_sleep:
        await asyncio.sleep(0.25) # when the "await" is blocking, the kernel switches to running other things in parallel
                                 # two tasks will only take about 0.25 seconds, being in parallel
    else:
        sleep(0.25) # but this blocks the thread, so two tasks will take 2*0.25 seconds
    return f"Transformed {key}"

async def do_work(use_async_sleep: bool):
    tasks = [f1('big_data', use_async_sleep), f1('cool_data', use_async_sleep)]
    return await asyncio.gather(*tasks)

async def time_the_work(use_async_sleep: bool):
    tic = datetime.datetime.now()
    res = await do_work(use_async_sleep) # can await inside an event loop, but cannot nest calls to asyncio.run()
    toc = datetime.datetime.now()
    print(f"with {use_async_sleep=}, retrieved val={res}, time elapsed = {toc-tic}")

asyncio.run(time_the_work(use_async_sleep=True))
asyncio.run(time_the_work(use_async_sleep=False))

print("Section 4: create_task\n\n")
"""
Should start the task's coroutine running immediately without
waiting until run() is called
"""
async def create_eager_tasks():
    print("Creating tasks...")
    # had the tasks list just been the f1 coroutines themselves, then they
    # would only have looged "Inside task" to stdout _after_ asyncio.run()
    # was called.
    tasks = [asyncio.create_task(co) for co in (f1('cool'), f1('dude'))]
    await asyncio.sleep(0.1)
    print(f"Now awaiting them")
    # note the special processing needed, right below, because I'm returning
    # a generator (an async generator)
    return (await t for t in tasks) 


async def process_tasks():
    generator = await create_eager_tasks()
    async for res in generator:
        print(res)

asyncio.run(process_tasks())

print("Section 5: Demo with HTTP requests\n\n")

"""
This just ties it all together, seeing how a batch of actual IO/network bound tasks goes faster when 
bunched together with asyncio
"""

async def get_internet():
    tic = datetime.datetime.now()
    async with aiohttp.ClientSession() as sess:
        async with sess.get("http://example.com") as response:
            val = "illustrative examples" in await response.text() # text() itself returns a coroutine
            toc = datetime.datetime.now()
            print(f"internet_time={toc-tic}")
            return val

async def scrape_internet():
    tic = datetime.datetime.now()
    tasks = [asyncio.create_task(get_internet()) for _ in range(5)]
    res = await asyncio.gather(*tasks)
    toc = datetime.datetime.now()
    # takes only about as long as the slowest request, plus tiny overhead not the sum of latencies
    print(f"Scraping internet took {toc-tic} (with asyncio!). Results = {res}")

asyncio.run(scrape_internet())
