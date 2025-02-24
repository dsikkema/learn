"""
Divide up merge_sort into chunks for multiprocessing. First tried processes = number of cores, but 
hardcoding 4 was better. Overall the parallel process, even though being able to take advantage of
multiple cores for this "CPU-bound" problem, still does worse than my single-threaded python merge_sort 
because of who knows how many reasons - memory access predictability, context-switching, cache invalidation,
layers of copying, synchronization overhead on the shared memory Array object...

 $ python core_fitting_merge_sort.py
system sort time: 0.11
multiprocess sort time: 3.11
single-threaded merge_sort sort time: 1.85

Father, I have failed.
"""
import pytest
import logging
from random import randint
from typing import Union
from multiprocessing import Process, Array, cpu_count
from math import ceil
from merge_sort import merge_sort as single_threaded_merge_sort

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
 

def multiway_merge(lists: list[Array], in_place_arr: Array) -> None:
    """
    Assumes input arrays are sorted, merges them together by writing in-place to in_place_arr param.
    """
    if not isinstance(lists, list):
        lists = list(lists)
    
    lists = [l for l in lists if l] # no nones, empties in list of lists

    n_lists = len(lists)
    sum_lens = sum(len(l) for l in lists)

    idxs = [0 for _ in range(n_lists)]
    # loop for the total number of items in all lists
    for in_place_idx in range(sum_lens):
        min_n = None
        min_l = None
        # find which non-exhausted list has the smallest next value
        for i, l in enumerate(lists):
            # while in the outer loop, there should always be at least one non-empty list to
            # trigger setting new minimums
            if min_n is None or l[idxs[i]] < min_n:
                min_n = l[idxs[i]]
                min_l = i

        in_place_arr[in_place_idx] = lists[min_l][idxs[min_l]]

        idxs[min_l] += 1

        if idxs[min_l] == len(lists[min_l]):
            lists.pop(min_l)
            idxs.pop(min_l)



def merge_sort(ls: list[int]):
    # cpu_count on my machine is 14; using 4 cores empirically does better.

    # n_processes = cpu_count()
    n_processes = 4 
    # convert to arrays for use in processes
    arrays = [Array('i', a) for a in split_list_evenly(ls, n_processes)] 
    processes = []
    for a in arrays:
        p = Process(target=merge_sort_arr, args=[a])
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()
    # convert arrays back to lists before merging
    multiway_merge([list(a) for a in arrays], ls)
    return ls

def merge_sort_arr(arr):
    """
    Sorts input array in-place 
    """
    # catch the outermost process call: convert to list for processing then back to array for memshare IPC
    if not isinstance(arr, list):
        ls = list(arr)
        merge_sort_arr(ls)
        for i, v in enumerate(ls):
            arr[i] = v
        return

    if len(arr) < 2:
        return

    idx = len(arr) // 2
    a = arr[:idx]
    b = arr[idx:]
    merge_sort_arr(a)
    merge_sort_arr(b)
    multiway_merge([a, b], arr)

    

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
    assert list(merge_sort(ls)) == expected

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
    out_arr = Array('i', [0] * len(expected))
    array_lists = [Array('i', l) for l in lists]
    multiway_merge(array_lists, out_arr)
    assert list(out_arr) == expected

def test_100_len_sort():
    src = [randint(0, 1000) for _ in range(100)]
    assert list(merge_sort(src)) == sorted(src)



def demo_sort_methods():
    """
    Compare performance between native sort, my single-threaded mergesort, and
    this multiprocess implementation.
    """
    src = [randint(0, 1000000) for _ in range(1000000)]
    
    from time import time
    tic = time()

    # sort with Python built-in function
    # sorted is not in-place
    expected_sorted = sorted(src) 
    toc = time()
    print(f"system sort time: {toc-tic:.2f}")

    src_copy = src.copy() # since merge_sort operates in place, save it

    tic = time()
    actual_sorted = merge_sort(src)
    toc = time()
    assert actual_sorted == expected_sorted

    print(f"multiprocess sort time: {toc-tic:.2f}")
    
    tic = time()
    single_threaded_merge_sort(src_copy)
    toc = time()

    print(f"single-threaded merge_sort sort time: {toc-tic:.2f}")

if __name__ == "__main__":
    demo_sort_methods()