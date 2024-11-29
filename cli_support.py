import os
import sys
from functools import wraps


def graceful_keyboard_interrupt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\n\nKeyboard interrupt detected. Exiting...")
            print("\nGoodbye! 👋\n")
            sys.exit(1)
    return wrapper


def debugger_on_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            import pdb; pdb.set_trace()
            raise e
    return wrapper

class GracefulInterruptMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # Wrap all public methods with graceful_keyboard_interrupt
        for key, value in attrs.items():
            if callable(value) and not key.startswith('_'):
                attrs[key] = graceful_keyboard_interrupt(value)
        return super().__new__(cls, name, bases, attrs)
    
    
class DebuggerOnErrorMetaclass(type):
    def __new__(cls, name, bases, attrs):
        for key, value in attrs.items():
            if callable(value) and not key.startswith('_'):
                attrs[key] = debugger_on_error(value)
        return super().__new__(cls, name, bases, attrs)