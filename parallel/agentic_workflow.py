from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
import subprocess










def run_command(cmd):
    """Runs a command and returns its stdout output."""
    # Handle both string commands and list commands
    if isinstance(cmd, list) and len(cmd) == 1:
        cmd = cmd[0]  # Extract the command string from the list
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    return cmd, result.stdout.strip(), result.stderr.strip()



def make_runner(task):
    """Makes a runner for a task."""
    def runner():
        return task.fn(*task.args, **task.kwargs)
    return runner


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


@dataclass
class Task:
    fn: str
    id: str = ''
    args: list[Binding] = []
    kwargs: dict[str, Binding] = {}
    postprocess: Callable = make_identity()
    ready: bool = False
    completed: bool = False
    output: str = ''
    yielder: bool = False
    
    def resolve_bindings(self):
        """Resolves bindings in a task."""
        self.args = [binding.resolve() for binding in self.args]
        self.kwargs = {k: binding.resolve() for k, binding in self.kwargs.items()}
        return self


def say_hello(): return 'Hello, World!'
def say_another(): return 'Another hello world'
def add_thanks(x): return f'{x} thanks'
def merge(x, y): return f'{x}\n\n{y}'
def echo(x, after_both=''): return x + y

hello = Task(
    fn=say_hello,
    ready=True,
)
another = Task(
    fn=say_another,
    ready=True,
)
after_hello = Task(
    fn=add_thanks,
    args=[Binding(hello, make_identity())],
    ready=True,
)
after_another = Task(
    fn=add_thanks,
    args=[Binding(another, make_identity())],
)
after_both = Task(
    fn=merge,
    args=[Binding(another, make_identity()), Binding(after_hello, make_identity())],
)
final = Task(
    fn=echo,
    args=[Binding(after_another, make_identity())],
    kwargs={'after_both': Binding(after_both, make_identity())},
)

for var in locals().values():
    if isinstance(var, Task):
        var.id = var.__name__

print(locals())
#tasks = [var for var in locals().values() if isinstance(var, Task)]




def mark_tasks_whose_dependencies_are_satisfied_as_ready(tasks):
    """Marks tasks whose dependencies are satisfied as ready."""
    for task in tasks:
        if task.ready: continue
        task.ready = all(binding.ready for binding in task.inputs)


# Run commands in parallel with dependency management
with ThreadPoolExecutor() as executor:
    future_to_task = {}
    
    def run_ready_tasks():
        for task in filter(lambda t: t.ready, tasks):
            task.resolve_bindings()
            runner = make_runner(task)
            new_future = executor.submit(runner)
            future_to_task[new_future] = task
    
    # Start with initial batch of commands that have no dependencies
    run_ready_tasks()
    
    while True:
        for future in as_completed(future_to_task): # Wait for the next completed future
            task = future_to_task.pop(future)
            task.output = task.postprocess(future.result())
            task.completed = True
            mark_tasks_whose_dependencies_are_satisfied_as_ready(tasks)
            run_ready_tasks()