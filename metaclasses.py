from functools import wraps
import inspect

# ------------------------------
# Registry for AutoRegistry
# ------------------------------
_registry = {}

def get_registry():
    return dict(_registry)

# ------------------------------
# Singleton (standard & lazy)
# ------------------------------
class Singleton(type):
    """Ensure only one instance per class."""
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class LazySingleton(Singleton):
    """Lazy instantiation of singleton (inherits Singleton logic)."""
    pass

class SingletonByArgs(type):
    """Singleton per unique args."""
    _instances = {}
    def __call__(cls, *args, **kwargs):
        key = (cls, args, tuple(sorted(kwargs.items())))
        if key not in cls._instances:
            cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]

# ------------------------------
# AutoInstantiate & AutoRegistry
# ------------------------------
class AutoInstantiate(type):
    """Instantiate class immediately on definition."""
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._instance = cls()

class AutoRegistry(type):
    """Automatically register classes in global registry."""
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        _registry[name] = cls

# ------------------------------
# Convert methods
# ------------------------------
class AllStaticMethods(type):
    """Make all methods static by default."""
    def __new__(mcls, name, bases, ns):
        for k, v in ns.items():
            if callable(v):
                ns[k] = staticmethod(v)
        return super().__new__(mcls, name, bases, ns)

class AutoProperties(type):
    """Convert get_* methods into @property."""
    def __new__(mcls, name, bases, ns):
        for k, v in list(ns.items()):
            if callable(v) and k.startswith("get_"):
                ns[k[4:]] = property(v)
        return super().__new__(mcls, name, bases, ns)

class AutoSlots(type):
    """Generate __slots__ from class attributes."""
    def __new__(mcls, name, bases, ns):
        slots = [k for k, v in ns.items() if not callable(v) and not k.startswith("__")]
        ns["__slots__"] = slots
        return super().__new__(mcls, name, bases, ns)

# ------------------------------
# Hooks & logging
# ------------------------------
class AutoHooks(type):
    """Wrap methods with before() and after() hooks."""
    def __new__(mcls, name, bases, ns):
        for k, v in ns.items():
            if callable(v) and not k.startswith("__"):
                ns[k] = mcls._wrap(v)
        return super().__new__(mcls, name, bases, ns)

    @staticmethod
    def _wrap(f):
        @wraps(f)
        def wrapper(*a, **kw):
            self = a[0]
            if hasattr(self, 'before'): self.before(f.__name__, *a, **kw)
            r = f(*a, **kw)
            if hasattr(self, 'after'): self.after(f.__name__, r)
            return r
        return wrapper

class MethodLogger(type):
    """Log all method calls with arguments and results."""
    def __new__(mcls, name, bases, ns):
        for k, v in ns.items():
            if callable(v) and not k.startswith("__"):
                ns[k] = mcls._log(v)
        return super().__new__(mcls, name, bases, ns)

    @staticmethod
    def _log(f):
        @wraps(f)
        def wrapper(*a, **kw):
            print(f"[MethodLogger] {f.__name__} called args={a[1:]}, kwargs={kw}")
            r = f(*a, **kw)
            print(f"[MethodLogger] {f.__name__} returned {r}")
            return r
        return wrapper

# ------------------------------
# Graceful keyboard interrupt / debugger
# ------------------------------
class GracefulInterrupt(type):
    """Wrap all public methods to handle KeyboardInterrupt gracefully."""
    def __new__(mcls, name, bases, ns):
        from cli_support import graceful_keyboard_interrupt
        for k, v in ns.items():
            if callable(v) and not k.startswith("_"):
                ns[k] = graceful_keyboard_interrupt(v)
        return super().__new__(mcls, name, bases, ns)

class DebuggerOnError(type):
    """Wrap public methods to enter debugger on exception."""
    def __new__(mcls, name, bases, ns):
        from cli_support import debugger_on_error
        for k, v in ns.items():
            if callable(v) and not k.startswith("_"):
                ns[k] = debugger_on_error(v)
        return super().__new__(mcls, name, bases, ns)

# ------------------------------
# Utility: copy class
# ------------------------------
def copy_class(cls, new_name):
    """Return a shallow copy of a class under a new name."""
    return type(new_name, cls.__bases__, dict(cls.__dict__))
