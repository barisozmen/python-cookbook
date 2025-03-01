from collections.abc import Callable


# transformer functions
def make_identity(): return lambda x: x
def make_picker(k): return lambda x: x[k]
def make_merger(): return lambda *x: '\n\n'.join(x)


    
class Binding:
    def __init__(self, source, transformer=make_identity()):
        self.source = source
        self.transformer = transformer
    def resolve(self):
        return self.transformer(self.source.output)


class Task:
    def __init__(
        self, 
        fn: Callable, 
        name: str = '',
        fn_args: list[Binding] = None,
        fn_kwargs: dict[str, Binding] = None, 
        postprocess: Callable = make_identity(), 
        ready: bool = False, 
        yielder: bool = False,
        
        # state variables
        completed=False,
        num_runs=0,
    ):
        self.fn = fn
        self._name = name
        self.fn_args = fn_args or []
        self.fn_kwargs = fn_kwargs or {}
        self.postprocess = postprocess
        self.ready = ready
        self.yielder = yielder
        
        # state variables
        self.completed = completed
        self.num_runs = num_runs
        
    @property
    def name(self):
        if not self._name:
            return self.fn.__name__
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def output(self):
        return self.postprocess(self.output_before_postprocess)
    
    @output.setter
    def output(self, value):
        self.output_before_postprocess = value
        
    def resolve_bindings(self):
        """Resolves bindings in a task."""
        self.fn_args = [binding.resolve() for binding in self.fn_args]
        self.fn_kwargs = {k: binding.resolve() for k, binding in self.fn_kwargs.items()}
        return self
    
    def __str__(self):
        return f'{self.name} - {self.fn.__name__}()'