import ctypes
import inspect

def modify_local_of_caller_frame():
    frame = inspect.currentframe()
    
    # Modify the locals dictionary
    frame.f_locals['x'] = 42
    
    # Sync the change to fast locals
    ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(frame), ctypes.c_int(0))


x=5
print(x, '<--before')
modify_local_of_caller_frame()
print(x, '<--after')
