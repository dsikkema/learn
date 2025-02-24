"""
Bad because of exponential process creation. Next: use thread pool fixed to number of cores.
"""
import pytest
import logging
from random import randint
from typing import Union
from multiprocessing import Process, Array, cpu_count
from math import ceil

def split_list_evenly(ls: list[int], n_splits: int) -> list[list[int]]:
    """
    Note: may not actually respect requested n_splits if it doesn't make sense, but tries. 
    """

    # 8/3 -> 3
    # 4/3 -> 2
    split_sz = ceil(len(ls) / n_splits)
    res = []
    for split_no in range(n_splits):
        start_idx = split_no * split_sz
        split = ls[start_idx: start_idx + split_sz]
        # possible that len(ls) divides evenly by split_sz from ceil(len/n_splits)
        if split:
            res.append(split)
    return res
 
@pytest.mark.parametrize(
    "ls, n_splits, expected",
    [
        ([1, 2, 3], 1, [[1, 2, 3]]),
        ([1, 2, 3], 2, [[1, 2], [3]]),
        ([1, 2, 3], 3, [[1], [2], [3]]),
        ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),
        ([1, 2, 3, 4], 3, [[1, 2], [3, 4]]),
        ([1, 2, 3, 4, 5, 6, 7, 8], 3, [[1, 2, 3], [4, 5, 6], [7, 8]]),
        ([1, 2, 3, 4, 5, 6, 7, 8], 14, [[1], [2], [3], [4], [5], [6], [7], [8]]),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 14, [[1], [2], [3], [4], [5], [6], [7], [8], [9]]),
    ]
)
def test_split(ls, n_splits, expected):
    assert split_list_evenly(ls, n_splits) == expected

def multiway_merge(lists: list[list[int]]) -> list[int]:
    """
    Assumes lists are sorted, merges them together
    """
    if not isinstance(lists, list):
        lists = list(lists)
    
    lists = [l for l in lists if l] # no nones, empties in list of lists

    n_lists = len(lists)
    sum_lens = sum(len(l) for l in lists)

    idxs = [0 for _ in range(n_lists)]
    result = []
    # loop for the total number of items in all lists
    for _ in range(sum_lens):
        min_n = None
        min_l = None
        # find which non-exhausted list has the smallest next value
        for l in lists:
            # while in the outer loop, there should always be at least one non-empty list to
            # trigger setting new minimums
            if min_n is None or l[0] < min_n:
                min_n = l[0]
                min_l = l
        # pop value to place on result, eliminate sublist if it's exhausted
        result.append(min_l.pop(0)) # should be equivalent to append(min_n)
        if not min_l:
            # only time there's an empty list is if we just _made_ one empty with the pop
            lists.remove([]) 
    
    return result

@pytest.mark.parametrize("lists, expected", [
    ([[1, 3], [2, 4]], [1, 2, 3, 4]),
    (
            ([], [1, 3]), [1, 3]
    ),
    (
            ([1, 3], []), [1, 3]
    ),
    (
            ([1, 3], [1, 2, 3]), [1, 1, 2, 3, 3]
    ),
    (
            ([1, 2, 3], [1, 5]), [1, 1, 2, 3, 5]
    ),
    (
            ([1, 2, 3], [1, 5]), [1, 1, 2, 3, 5]
    ),
    (
            ([1, 2, 3], [0, 5]), [0, 1, 2, 3, 5]
    ),
    (
            ([1, 2, 3], [0, 5], [2, 6]), [0, 1, 2, 2, 3, 5, 6]
    ),
    (
            ([1, 2, 3], [-1, 88], [0, 5], [2, 6]), [-1, 0, 1, 2, 2, 3, 5, 6, 88]
    ),
    (
            ([5], [1, 2, 3], [-1, 88], [0, 5], [2, 6]), [-1, 0, 1, 2, 2, 3, 5, 5, 6, 88]
    ),
])
def test_multiway_merge(lists, expected):
    assert multiway_merge(lists) == expected


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

def merge_sort(ls: list[int]) -> list[int]:
    n_cores = cpu_count()
    lists = split_list_evenly(ls, n_cores)
    sorted_arrays = []
    processes = []
    for l in lists:
        arr = Array('i', l)
        p = Process(target=merge_sort_arr, args=[arr])
        p.start()
        sorted_arrays.append(arr)
        processes.append(p)
    
    for p in processes:
        p.join()
    
    return multiway_merge([list(arr) for arr in sorted_arrays])

def merge_sort_arr(arr):
    res = merge_sort_sublist(list(arr))
    for i, v in enumerate(res):
        arr[i] = v

def merge_sort_sublist(ls):
    
    if len(ls) < 2:
        return ls

    idx = len(ls) // 2
    a = merge_sort_sublist(ls[:idx])
    b = merge_sort_sublist(ls[idx:])
    return multiway_merge((a, b))

def test_very_large_sort():
    """
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
