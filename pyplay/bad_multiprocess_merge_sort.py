"""
Bad because of exponential process creation. Next: use thread pool fixed to number of cores.
"""
import pytest
import logging
from random import randint
from typing import Union
from multiprocessing import Process, Array

def merge(a, b):
    assert None not in (a, b)
    if len(a) == 0:
        return b
    elif len(b) == 0:
        return a
    
    i_a, i_b = 0, 0
    result = []

    while i_a < len(a) or i_b < len(b):
        cur_a, cur_b = None, None
        if i_a < len(a):
            cur_a = a[i_a]
        if i_b < len(b):
            cur_b = b[i_b]

        if cur_a is not None and cur_b is not None:
            if cur_a <= cur_b: # cur_b None implies only a is left
                result.append(cur_a)
                i_a += 1
            else:
                result.append(cur_b)
                i_b += 1
        else:
            if cur_a is None:
                result.append(cur_b)
                i_b += 1
            else:
                result.append(cur_a)
                i_a += 1


    return result

def merge_sort_arr(arr: Array):
    """
    Results in an in-place sort of arr (but by means of inefficient copying into separate list structure, then
    writing back to the original array)
    """

    ls = list(arr)
    if len(ls) < 2:
        return ls

    idx = len(ls) // 2
    arr_a = Array('i', ls[:idx])
    arr_b = Array('i', ls[idx:])
    p_a = Process(target=merge_sort_arr, args=[arr_a])
    p_b = Process(target=merge_sort_arr, args=[arr_b])
    p_a.start()
    p_b.start()
    p_a.join()
    p_b.join()

    res = merge(list(arr_a), list(arr_b))
    for i, v in enumerate(res):
        arr[i] = v

def merge_sort(ls: list[int]):
    arr = Array('i', ls)
    merge_sort_arr(arr)
    return list(arr)

def test_very_large_sort():
    """
    When running with `pytest multiprocess_merge_sort.py::test_very_large_sort -s` (to see printed output) we
    see the multiprocessing version takes a huge amount of extra time. It wasn't expected to really go much
    faster (except possibly by taking advantage of multiple cores) because the operation is CPU-bound. But
    the process overhead (and exponential creation of processe) is a huge drag.

    ```
    multiprocess_merge_sort.py system sort time: 0.00
    multiprocess sort time: 1.92
    ```
    """
    src = [randint(0, 1000000) for _ in range(100)]
    
    from time import time
    tic = time()

    # sort with Python built-in function
    # sorted is not in-place
    expected_sorted = sorted(src) 
    toc = time()
    print(f"system sort time: {toc-tic:.2f}")

    tic = time()
    actual_sorted = merge_sort(src)
    toc = time()
    print(f"multiprocess sort time: {toc-tic:.2f}")
    assert actual_sorted == expected_sorted


@pytest.mark.parametrize("a, b, expected", [
    ([1, 3], [2, 4], [1, 2, 3, 4]),
    (
            [], [1, 3], [1, 3]
    ),
    (
            [1, 3], [], [1, 3]
    ),
    (
            [1, 3], [1, 2, 3], [1, 1, 2, 3, 3]
    ),
    (
            [1, 2, 3], [1, 5], [1, 1, 2, 3, 5]
    ),
    (
            [1, 2, 3], [1, 5], [1, 1, 2, 3, 5]
    ),
    (
            [1, 2, 3], [0, 5], [0, 1, 2, 3, 5]
    ),
])
def test_merge(a, b, expected):
    assert merge(a, b) == expected

@pytest.mark.parametrize("ls, expected", [
    ([], []),
    ([1], [1]),
    ([1, 2], [1, 2]),
    ([2, 1], [1, 2]),
    ([2, 1, 3], [1, 2, 3]),
    ([2, 3, 1], [1, 2, 3]),
    ([1, 2, 3], [1, 2, 3]),
    ([1, 3, 2], [1, 2, 3]),
    ([3, 2, 1], [1, 2, 3]),
    ([3, 1, 2], [1, 2, 3]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([4, 3, 2, 1], [1, 2, 3, 4]),
    ([1, 3, 2, 4], [1, 2, 3, 4]),
    ([4, 3, 2, 1], [1, 2, 3, 4]),
    ([4, 2, 3, 1], [1, 2, 3, 4]),
    ([4, 4], [4, 4]),
    ([4, 4, 4], [4, 4, 4]),
    ([1, 4, 4, 4, 5], [1, 4, 4, 4, 5]),
    ([5, 4, 4, 4, 1], [1, 4, 4, 4, 5]),
])
def test_merge_sort(ls, expected):
    assert merge_sort(ls) == expected
