def flatten(l):
    """Flattens a list recursively.
    
    This function will recursively flatten nested lists to any depth.
    Example: flatten([1, [2, [3, 4]], 5]) -> [1, 2, 3, 4, 5]
    """
    result = []
    for item in l:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# https://youtu.be/RZ4Sn-Y7AP8?t=1353
import sys, difflib
def diff(fromfile, tofile):
    fromlines = open(fromfile).readlines()
    tolines = open(tofile).readlines()
    diff = difflib.context_diff(fromlines, tolines, fromfile, tofile)
    sys.stdout.writelines(diff)



def test_flatten():
    # Basic nested list
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
    # Empty list
    assert flatten([]) == []
    # List with empty nested lists
    assert flatten([[], [[]], [[], []]]) == []
    # Deeply nested structure
    assert flatten([1, [2, [3, [4, [5]]]]]) == [1, 2, 3, 4, 5]
    # Mixed data types
    assert flatten(["a", ["b", ["c"]], 1, [2]]) == ["a", "b", "c", 1, 2]
    # Non-nested list
    assert flatten([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    print('test_flatten passed')
    
if __name__ == '__main__':
    [f() for f in globals().copy().values() if callable(f) and f.__name__.startswith('test_')]
