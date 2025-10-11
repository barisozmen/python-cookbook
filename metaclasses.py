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



from functools import wraps
import weakref
import time

# ------------------------------
# TypeEnforcedMetaclass
# ------------------------------
class TypeEnforced(type):
    """Enforce type hints at runtime."""
    def __new__(mcls, name, bases, ns):
        for k, v in ns.items():
            if callable(v) and not k.startswith("__"):
                ns[k] = mcls._enforce_types(v)
        return super().__new__(mcls, name, bases, ns)

    @staticmethod
    def _enforce_types(f):
        hints = getattr(f, '__annotations__', {})
        @wraps(f)
        def wrapper(*args, **kwargs):
            bound = inspect.signature(f).bind(*args, **kwargs)
            bound.apply_defaults()
            for arg, val in bound.arguments.items():
                if arg in hints and not isinstance(val, hints[arg]):
                    raise TypeError(f"{arg} must be {hints[arg]}, got {type(val)}")
            return f(*args, **kwargs)
        return wrapper

# ------------------------------
# CachedMetaclass
# ------------------------------
class Cached(type):
    """Cache all method calls based on args/kwargs."""
    def __new__(mcls, name, bases, ns):
        for k, v in ns.items():
            if callable(v) and not k.startswith("__"):
                ns[k] = mcls._cache(v)
        return super().__new__(mcls, name, bases, ns)

    @staticmethod
    def _cache(f):
        store = {}
        @wraps(f)
        def wrapper(*a, **kw):
            key = (a, tuple(sorted(kw.items())))
            if key not in store:
                store[key] = f(*a, **kw)
            return store[key]
        return wrapper

# ------------------------------
# EventMetaclass
# ------------------------------
class EventMetaclass(type):
    """Broadcast events before and after method execution."""
    def __new__(mcls, name, bases, ns):
        for k, v in ns.items():
            if callable(v) and not k.startswith("__"):
                ns[k] = mcls._wrap_event(v)
        return super().__new__(mcls, name, bases, ns)

    @staticmethod
    def _wrap_event(f):
        @wraps(f)
        def wrapper(*a, **kw):
            self = a[0]
            if hasattr(self, 'on_event'):
                self.on_event(f.__name__, "before", *a, **kw)
            result = f(*a, **kw)
            if hasattr(self, 'on_event'):
                self.on_event(f.__name__, "after", result)
            return result
        return wrapper

# ------------------------------
# AutoDocMetaclass
# ------------------------------
class AutoDoc(type):
    """Automatically generate docstrings listing methods."""
    def __new__(mcls, name, bases, ns):
        method_list = [k for k, v in ns.items() if callable(v) and not k.startswith("__")]
        ns.setdefault("__doc__", f"{name} methods: {', '.join(method_list)}")
        return super().__new__(mcls, name, bases, ns)

# ------------------------------
# ObservableMetaclass
# ------------------------------
class Observable(type):
    """Make class attributes observable via callbacks."""
    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)
        cls._observers = weakref.WeakSet()
        return cls

    def __setattr__(cls, key, value):
        super().__setattr__(key, value)
        for obs in getattr(cls, "_observers", []):
            obs(cls, key, value)

    def bind(cls, observer):
        cls._observers.add(observer)

# ------------------------------
# TimeitMetaclass
# ------------------------------
class Timeit(type):
    """Measure execution time of all methods."""
    def __new__(mcls, name, bases, ns):
        for k, v in ns.items():
            if callable(v) and not k.startswith("__"):
                ns[k] = mcls._timeit(v)
        return super().__new__(mcls, name, bases, ns)

    @staticmethod
    def _timeit(f):
        @wraps(f)
        def wrapper(*a, **kw):
            start = time.time()
            result = f(*a, **kw)
            end = time.time()
            print(f"[Timeit] {f.__name__} executed in {end-start:.6f}s")
            return result
        return wrapper

# ------------------------------
# InterfaceEnforcerMetaclass
# ------------------------------
class InterfaceEnforcer(type):
    """Ensure class implements all required methods."""
    def __new__(mcls, name, bases, ns, required=None):
        cls = super().__new__(mcls, name, bases, ns)
        required = required or []
        for method in required:
            if not callable(getattr(cls, method, None)):
                raise TypeError(f"Class {name} must implement {method}()")
        return cls




# ------------------------------
# MetaToolkit factory
# ------------------------------
def MetaToolkit(*, behaviors=None):
    """Return a metaclass that combines multiple behaviors."""
    behaviors = behaviors or []

    class _Meta(type):
        def __new__(mcls, name, bases, ns):
            for behavior in behaviors:
                # Apply behavior's __new__ if it exists
                if hasattr(behavior, "__new__") and callable(behavior.__new__):
                    temp_cls = behavior.__new__(behavior, "Temp", (), dict(ns))
                    ns.update(temp_cls.__dict__)
            cls = super().__new__(mcls, name, bases, ns)
            # Call __init__ hooks if present (e.g., AutoInstantiate, AutoRegistry)
            for behavior in behaviors:
                if hasattr(behavior, "__init__") and callable(behavior.__init__):
                    behavior.__init__(cls, name, bases, ns)
            return cls

    return _Meta



# ------------------------------
# Utility: copy class
# ------------------------------
def copy_class(cls, new_name):
    """Return a shallow copy of a class under a new name."""
    return type(new_name, cls.__bases__, dict(cls.__dict__))





