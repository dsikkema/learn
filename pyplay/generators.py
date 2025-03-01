from collections.abc import Generator
from typing import Any
from random import random

print("\n\nBasic: delays executing body until first item retrieved\n")
def gen():
    print("Now, the generator runs")
    # can just call yield multiple times, control is passed back to calling env every time a yield is hit
    yield 1
    print("This is after yielding 1, before yielding 2")
    yield 2
    yield 3

my_gen = gen() # won't run generator body yet
print("called gen() to create generator")
for i in my_gen:
    print(f"In loop: got {i} from generator")

print("\n\nReading generator with next() directly")
def gen_quiet():
    yield 1
    yield 2
    yield 3
gen2 = gen_quiet()
print(next(gen2))
print(next(gen2))
print(next(gen2))

print("\n\nStopIteration exception automatically thrown when no more items (it's how loop knows when to be done)")
try:
    next(gen2)
    assert False # must throw exception and not get here
except StopIteration:
    print("Caught the stop iteration exception when no more items are available")


print("\n\nCan return a value when finished generation")
# I imagine this could be useful for something kind of like a "status code" for the end
# of generation. E.g., generation stopped because no records left vs all remaining recoreds
# are "not ready" in some way.

def gen_return():
    final = 7
    for i in range(3):
        yield i
    return final # injected into exception

g = gen_return()

# loop never accesses the "7" integer value
for i in g:
    print(i)

g = gen_return()

# if loop directly on generator then the loop itself will consume and disregard the return value in exception
next(g), next(g), next(g) 
try:
    next(g) # fourth tries throws exception...
    assert False # must throw exception and not get here
except StopIteration as e:
    val = e.value
    assert val
    print(f"Caught stop iteration exception with value: {val}")

# now try another next(), no more value. Only returns once.
try:
    next(g) # fourth tries throws exception...
except StopIteration as e:
    val = e.value
    assert not val # but now there's no value
    print(f"Caught stop iteration exception: {val=}")

print("\n\nGenerator expression, on-demand")

number_of_electrons_in_the_universe = 10**81
number_of_electrons_in_the_universe += 20 # just an estimate; err on the high side, just to be safe

def square(x):
    print(f"squaring {x=}")
    return x**2

squares = (square(x) for x in range(number_of_electrons_in_the_universe))

for _ in range(3):
    # sure is nice that the whole generator's range doesn't get computed and pulled into memory

    # I'm almost sure that fitting that many bits inside the confined space of my laptop would
    # create a black hole. Not certain, will not look into this today.

    print(f"getting the next square: {next(squares)}")


print("\n\nTimeline for yield and send():\n")

def timeline_example():
    """In this example, see output t=0, t=1, t=2, ... for timeline across both generator and caller."""

    # This makes clear a few things. On the first priming, next() or send(None), the generator starts
    # at the very top of its function body: there's no "yield" statement yet (even if yield is in "line
    # 1", the generator starts at "line 0") to receive the sent value. But after the first yield of the
    # generator, the next value sent will be "returned" by that same yield keyword (the one that "caught"
    # on sending the last value to caller) and execution resume until next yield

    def generator_with_timeline_annotation():
        """ see t=0, t=1, etc for timeline """
        print("t=0")
        {}[print("t=2")] = yield print("t=1")
        while True:
            print("t=3")
            {}[print("t=5")] = yield print("t=4")
            print("t=6")
            break

    g = generator_with_timeline_annotation()
    g.send(None)
    while True:
        try:
            g.send(1)
        except StopIteration:
            break

timeline_example()
    

print("\n\nCoroutine and cooperative communications: an exercise:\n")


# A different example
def high_eq_generator():
    print("LISTENER_INTERNAL_MONOLOGUE: They said a silent hello to me. I'll tell them I'm listening.")
    those_precious_syllables = yield "I am listening."

    while 6 < number_of_electrons_in_the_universe:
        print(f"LISTENER_INTERNAL_MONOLOGUE: Well, what they said was '{those_precious_syllables}'. Let me make sure I understand them and that they feel heard.")
        those_precious_syllables = yield f"What I'm hearing you say is '{those_precious_syllables}'. Is that what you mean?"

eq = high_eq_generator()
print(f"SPEAKER_INTERNAL_MONOLOGUE: I think I'll just look their way and say nothing.")
a_silent_hello = None
# necessary to send None for first invocation. It primes the generator to get the execution up to the first yield
first_reply = eq.send(a_silent_hello)
print(f"SPEAKER_INTERNAL_MONOLOGUE: Ok, I said '{a_silent_hello}', then they said '{first_reply}'")
for idea in ["I'm hungry", "I want to watch a movie", "The AC is too low"]:
    print(f"SPEAKER_INTERNAL_MONOLOGUE: I think {idea}, therefore I'm going to say it")
    print(f"Speaker: '{idea}'")
    response = eq.send(idea)
    print(f"\nListener: '{response}'\n")

print("\n\nType annotation for generator\n\n")

# Generator[YieldType, SendType, ReturnType]
def to_int_gen() -> Generator[int, float, str]: 
    sent = yield
    assert isinstance(sent, float)
    for _ in range(3):
        sent = yield int(sent)
    return 'I am a string'
        
g = to_int_gen()
g.send(None)
for f in (float(ord(c) * random()) for c in 'lol'):
    print(f"{f} -> {g.send(f)}")

final_return = None
try:
    g.send(float(sum(ord(c) for c in 'lol')))
except StopIteration as e:
    final_return = e.value
assert isinstance(final_return, str)

print("\n\nChain and Pipeline examples\n")

def gen_x():
    for i in [0, 1, 2, 3, 4, 5]:
        yield i

def gen_z():
    for i in [9, 10]:
        yield i

def two_to_N(items):
    for i in items:
        yield 2**i

def only_even(items):
    for i in items:
        if i % 2 == 0:
            yield i

def combined_gen():
    # concatenates x then z
    yield from gen_x()
    yield from gen_z()

chain = combined_gen()
chain = only_even(chain)
chain = two_to_N(chain)
for i in chain:
    print(i)