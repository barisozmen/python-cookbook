import ctypes
import inspect

def modify_locals():
    frame = inspect.currentframe()
    # Modify the locals dictionary
    frame.f_locals['x'] = 42
    # Sync the change to fast locals
    ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(frame), ctypes.c_int(0))
    print(x)  # Now x is 42 in this scope!


x=5
print(x, '<--before')
modify_locals()
print(x, '<--after')
