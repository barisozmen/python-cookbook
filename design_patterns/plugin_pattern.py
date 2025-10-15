# https://chatgpt.com/share/68ef33f3-9304-8010-bc6a-88773ccea1b4

import uuid
from functools import wraps
from collections import defaultdict
from contextvars import ContextVar
import inspect
import asyncio

# ----------------------------
# Base Pluggable class
# ----------------------------
class Pluggable:
    registry = {}
    current_context: ContextVar[dict] = ContextVar('current_context', default={})

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Pluggable.registry[cls.__name__] = cls

    async def before(self, func=None, call_id=None, *args, **kwargs): pass
    async def on_success(self, func=None, call_id=None, result=None, *args, **kwargs): pass
    async def on_error(self, func=None, call_id=None, exception=None, *args, **kwargs): pass
    async def finally_(self, func=None, call_id=None, *args, **kwargs): pass

# ----------------------------
# Runtime plugin registry
# ----------------------------
_runtime_plugs = defaultdict(list)

# ----------------------------
# Helper to call a hook (await if async)
# ----------------------------
async def _maybe_await(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)

# ----------------------------
# Helper to call all plugin hooks concurrently
# ----------------------------
async def _run_hooks_concurrently(plugs, hook_name, **kwargs):
    tasks = [_maybe_await(getattr(p(), hook_name), **kwargs) for p in plugs]
    if tasks:
        await asyncio.gather(*tasks)

# ----------------------------
# Unified Plug decorator / context manager
# ----------------------------
class Plug:
    def __init__(self, *targets):
        self.targets = [Pluggable.registry[t] if isinstance(t, str) else t for t in targets]
        self._wrapped_functions = []

    def __call__(self, func):
        _runtime_plugs[func].extend(self.targets)
        self._wrapped_functions.append((func, self.targets.copy()))

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            call_id = uuid.uuid4()
            token = Pluggable.current_context.set({'call_id': call_id})
            try:
                # BEFORE hooks concurrently
                await _run_hooks_concurrently(_runtime_plugs[func], "before", func=func, call_id=call_id, *args, **kwargs)

                # Execute function
                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)

                # ON_SUCCESS hooks concurrently
                await _run_hooks_concurrently(_runtime_plugs[func], "on_success", func=func, call_id=call_id, result=result, *args, **kwargs)

                return result
            except Exception as e:
                # ON_ERROR hooks concurrently
                await _run_hooks_concurrently(_runtime_plugs[func], "on_error", func=func, call_id=call_id, exception=e, *args, **kwargs)
                raise
            finally:
                # FINALLY hooks concurrently
                await _run_hooks_concurrently(_runtime_plugs[func], "finally_", func=func, call_id=call_id, *args, **kwargs)
                Pluggable.current_context.reset(token)

        # Return sync wrapper if original function is sync
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                return asyncio.run(async_wrapper(*args, **kwargs))
            return sync_wrapper