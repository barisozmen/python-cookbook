
# https://youtu.be/RZ4Sn-Y7AP8?t=1434
def filetypes(topdir):
    from collections import Counter
    from pprint import pprint
    
    c = Counter(os.path.splitext(name)[1] 
                for name in allfiles(topdir))
    pprint(c.most_common())


# https://youtu.be/RZ4Sn-Y7AP8?t=1353
import sys, difflib
def diff(fromfile, tofile):
    fromlines = open(fromfile).readlines()
    tolines = open(tofile).readlines()
    diff = difflib.context_diff(fromlines, tolines, fromfile, tofile)
    sys.stdout.writelines(diff)


# https://youtu.be/RZ4Sn-Y7AP8?t=1463
def find(topdir, pattern):
    from fnmatch import fnmatch
    return ((path, name)
            for path, name in allfiles(topdir)
            if fnmatch(name, pattern))
