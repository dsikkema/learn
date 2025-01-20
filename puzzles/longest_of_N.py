"""
Given a string containing only lowercase letters, find the length of the longest substring that contains exactly two
distinct characters. For example, if the input is "ecebaaacd", the answer would be 4 - the substring "baaa". If the
input is "abcabcabc", the answer would be 2, as any substring with exactly two
distinct characters can only be length 2 in this case.

In this file I also use doctest (run with `pytest --doctest-modules module.py`), see the result function's
docstring defining test cases.

Also wrote a tiny logger contextmanager

Update: support n unique chars (and also, as before, return the string which comprises the match: namely the first such string found)
"""
from pathlib import Path
from contextlib import contextmanager

def f(string, n):
    assert n >= 2
    # using this cool logger because as long as I'm using pytest with doctest, I can't print debug output
    with logging() as logger:
        if len(string) < n:
            return None
        
        max_win_len = 0
        max_win = ""

        uniqs = list(
            (string[0])
        )

        uniq_pos = {string[0]: 0}
        window = string[0]
        i = 1

        """
        `i` always represents the index of the ending character of a sliding window. It always advances one-by-one, 
        checking each new character that comes into the window. When a N+1th  character is found, the beginning of the 
        window jumps forward just far enough so that the window only contains N characters again. And rolling max 
        updates happen every loop. `uniq_pos` is used to track the last position each character was found at, so that
        whenever that character "falls out" of the window, we know where to jump the window up to.
        
        Hence, `window` is always a string that consists of no more than N unique characters.         

        because we did length validation at the beginning of this function, if N uniq chars have not been found  at the end of the 
        loop, then then we are certain that an answer exists and we've found it
        """
        while i < len(string):
            c = string[i]
            if len(uniqs) < n and not c in uniqs:
                uniqs.append(c)

            if c in uniqs:
                window += c
            else:
                # The "oldest" character (beginning of list) is "pushed out" by the newly arrived character as we
                # scan through
                popped = uniqs.pop(0)
                popped_pos = uniq_pos[popped] 
                del uniq_pos[popped]
                uniqs.append(c)
                # To form a new window longer than the previous max would require going past the bounds of the string,
                # so quit early here
                if popped_pos + max_win_len + 2 > len(string):
                    logger.log("Breaking early")
                    break
                window = string[popped_pos + 1 : i + 1]

            uniq_pos[c] = i

            if len(window) > max_win_len:
                max_win_len = len(window)
                max_win = window

            i += 1
        if len(uniqs) < n:
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

    

def result(string, n = 2):
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
    >>> assert result("", 3) is None
    >>> assert result("a", 3) is None
    >>> assert result("ab", 3) is None
    >>> assert result("abb", 3) is None
    >>> assert result("aaa", 3) is None
    >>> result("abc", 3)
    (3, 'abc')
    >>> result("abcc", 3)
    (4, 'abcc')
    >>> result("abccc", 3)
    (5, 'abccc')
    >>> result("cabcc", 3)
    (5, 'cabcc')
    >>> result("cabcca", 3)
    (6, 'cabcca')
    >>> result("cabzcca", 3)
    (4, 'bzcc')
    >>> result("cabzzzzzca", 3)
    (7, 'abzzzzz')
    >>> result("abcdabcdabcdabccccc", 3)
    (7, 'abccccc')
    >>> result("abcdefghij", 10)
    (10, 'abcdefghij')
    >>> result("aabcdefghij", 10)
    (11, 'aabcdefghij')
    >>> result("abcdefghijj", 10)
    (11, 'abcdefghijj')
    >>> result("abcdeefghij", 10)
    (11, 'abcdeefghij')
    >>> assert result("abcd", 10) is None
    >>> assert result("abcdffffffffffffff", 10) is None
    >>> result("abcdefghijjjjjjjjjjjzz", 10)
    (21, 'bcdefghijjjjjjjjjjjzz')
    """

    return f(string, n)
