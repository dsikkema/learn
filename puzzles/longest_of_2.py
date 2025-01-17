"""
Given a string containing only lowercase letters, find the length of the longest substring that contains exactly two
distinct characters. For example, if the input is "ecebaaacd", the answer would be 4 - the substring "baaa". If the
input is "abcabcabc", the answer would be 2, as any substring with exactly two
distinct characters can only be length 2 in this case.

In this file I also use doctest (run with `pytest --doctest-modules module.py`), see the result function's
docstring defining test cases.

Also wrote a tiny logger contextmanager
"""
from pathlib import Path
from contextlib import contextmanager

def f(string):
    # using this cool logger because as long as I'm using pytest with doctest, I can't print debug output
    with logging() as logger:
        if len(string) <= 1:
            return None
        
        max_win_len = 0
        max_win = ""

        first = string[0]
        last_pos_first = 0
        window = first
        second = None
        i = 1
       
        """
        `i` always represents the index of the ending character of a sliding window. It always advances one-by-one, 
        checking each new character that comes into the window. When a third character is found, the beginning of the 
        window jumps forward just far enough so that the window only contains two characters again. And rolling max 
        updates happen every loop.
        
        Hence, `window` is always a string that consists of no more than two unique characters. `first` and `second` 
        represent the two characters which are the unique characters comprising the window. `second` is set when it's 
        found, and if it's never found then it means the string is only made of one character and has no answer.
        
        because we did length validation at the beginning of this function, if `second` is not None at the end of the 
        loop, then then we are certain that an answer exists and we've found it
        """
        while i < len(string):
            c = string[i]
            if second is None and c != first:
                second = c
            if c == first:
                last_pos_first = i
                window += c
            elif c == second:
                last_pos_second = i
                window += c
            else: # window now starts after the last instance of previous "first", until c
                first = second
                second = c
                
                if last_pos_first + max_win_len + 2 > len(string):
                    logger.log("Breaking early")
                    break

                window = string[last_pos_first + 1 : i + 1]
                last_pos_first = last_pos_second
                last_pos_second = i
            if len(window) > max_win_len:
                max_win_len = len(window)
                max_win = window

            i += 1
        if second is None:
            return None

        """
            # naive implementation
            for i in range(len(string) - 1):
                first = string[i]
                second = None
                window = first
                for c in string[i + 1 :]:
                    if second is None and c != first:
                        second = c
                    if c in (first, second):
                        window += c
                    else:
                        break
                if i == 0 and second is None:
                    return None
                if len(window) > max_win_len:
                    max_win_len = len(window)
                    max_win = window
            return max_win_len, max_win
        """
        return max_win_len, max_win

class Logger:
    def __init__(self, f):
        self.f = f
    def log(self, s):
        self.f.write(f"{s}\n")

@contextmanager
def logging():
    Path("logs").mkdir(exist_ok=True)
    with open("logs/out.log", 'a') as f:
        yield Logger(f)

    

def result(string):
    """
    >>> assert result("") is None
    >>> assert result("a") is None
    >>> assert result("aa") is None
    >>> assert result("aaa") is None
    >>> result("ab")
    (2, 'ab')
    >>> result("aab")
    (3, 'aab')
    >>> result("aaab")
    (4, 'aaab')
    >>> result("aaaba")
    (5, 'aaaba')
    >>> result("aaabaa")
    (6, 'aaabaa')
    >>> result("aaabaab")
    (7, 'aaabaab')
    >>> result("aaabaaba")
    (8, 'aaabaaba')
    >>> result("aaabzaaba")
    (4, 'aaab')
    >>> result("aaabzaabaa")
    (5, 'aabaa')
    >>> result("abcdefgg")
    (3, 'fgg')
    >>> result("abcdefggh")
    (3, 'fgg')
    >>> result("abcdefgghh")
    (4, 'gghh')
    >>> result("aaaaaabbc")
    (8, 'aaaaaabb')
    >>> result("aaaaaabbbc")
    (9, 'aaaaaabbb')
    >>> result("aaaaaabbbcc")
    (9, 'aaaaaabbb')
    >>> result("aaaaaabbbccc")
    (9, 'aaaaaabbb')
    >>> result("aaaaaabbbcccc")
    (9, 'aaaaaabbb')
    >>> result("zaaaaaabbbcccc")
    (9, 'aaaaaabbb')
    >>> result("caaaaaabbbcccc")
    (9, 'aaaaaabbb')
    >>> result("ababcdcdefefghghghij")
    (6, 'ghghgh')
    """

    return f(string)
