import pytest

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

def merge_sort(ls):
    if len(ls) < 2:
        return ls

    idx = len(ls) // 2
    a = merge_sort(ls[:idx])
    b = merge_sort(ls[idx:])
    return merge(a, b)

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
