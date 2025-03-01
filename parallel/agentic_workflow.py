from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
import subprocess
from utils import flatten



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
        self.name = name
        self.fn_args = fn_args or []
        self.fn_kwargs = fn_kwargs or {}
        self.postprocess = postprocess
        self.ready = ready
        self.yielder = yielder
        
        # state variables
        self.completed = completed
        self.num_runs = num_runs
        
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
    
    
def say_hello(): return 'Hello, World!'
def say_another(): return 'Another hello world'
def add_thanks(x): return f'{x} thanks'
def merge(x, y): return f'{x}\n\n{y}'
def echo(x, after_both=''): return x + after_both

hello = Task(
    say_hello,
    ready=True,
)
another = Task(
    say_another,
    ready=True,
)
after_hello = Task(
    add_thanks,
    fn_args=[Binding(hello, make_identity())],
)
after_another = Task(
    add_thanks,
    fn_args=[Binding(another, make_identity())],
    yielder=True,
)
after_both = Task(
    merge,
    fn_args=[Binding(another, make_identity()), Binding(after_hello, make_identity())],
)
final = Task(
    echo,
    fn_args=[Binding(after_another, make_identity())],
    fn_kwargs={'after_both': Binding(after_both, make_identity())},
    yielder=True,
)
for k, v in locals().copy().items():
    if isinstance(v, Task):
        v.name = k
tasks = [v for v in locals().copy().values() if isinstance(v, Task)]


def print_task_graph_summary(tasks):
    """
    Prints a summary of the task dependency graph.
    
    Shows:
    - Overall dependency structure
    - Starting tasks (ready=True)
    - Yielding tasks (yielder=True)
    - Dependency chains
    """
    print("=== TASK DEPENDENCY GRAPH SUMMARY ===\n")
    
    # Find root tasks (those that start ready)
    root_tasks = [task for task in tasks if task.ready]
    yielding_tasks = [task for task in tasks if task.yielder]
    
    # Build dependency map
    dependency_map = {}
    for task in tasks:
        dependencies = []
        # Check args for dependencies
        for binding in task.fn_args:
            dependencies.append(binding.source)
        # Check kwargs for dependencies
        for binding in task.fn_kwargs.values():
            dependencies.append(binding.source)
        dependency_map[task] = dependencies
    
    # Build reverse dependency map (what depends on what)
    reverse_map = {task: [] for task in tasks}
    for task, deps in dependency_map.items():
        for dep in deps:
            if dep in reverse_map:  # Make sure the dependency exists in our task list
                reverse_map[dep].append(task)
    
    # Print overall structure
    print("Task Structure:")
    # Use a set to track tasks we've already processed to avoid duplicates
    processed_tasks = set()
    for task in tasks:
        # Skip if we've already processed this task (by name)
        if task.name in processed_tasks:
            continue
        processed_tasks.add(task.name)
        
        deps = dependency_map[task]
        dependents = reverse_map[task]
        
        # Format task info with special markers
        markers = []
        if task.ready:
            markers.append("ROOT")
        if task.yielder:
            markers.append("YIELDS")
        
        marker_str = f" [{', '.join(markers)}]" if markers else ""
        
        print(f"  {task.name}{marker_str}")
        if deps:
            print(f"    Depends on: {', '.join(d.name for d in deps)}")
        if dependents:
            print(f"    Required by: {', '.join(d.name for d in dependents)}")
    
    print("\nStarting Tasks:")
    # Use a set to track task names we've already processed
    processed_root_tasks = set()
    for task in root_tasks:
        if task.name not in processed_root_tasks:
            print(f"  {task.name} - {task.fn.__name__}()")
            processed_root_tasks.add(task.name)
    
    print("\nYielding Tasks:")
    # Use a set to track task names we've already processed
    processed_yielding_tasks = set()
    for task in yielding_tasks:
        if task.name not in processed_yielding_tasks:
            print(f"  {task.name} - {task.fn.__name__}()")
            processed_yielding_tasks.add(task.name)
    
    # Find execution paths
    print("\nExecution Paths:")
    
    def trace_path(task, path=None, visited=None):
        if path is None:
            path = []
        if visited is None:
            visited = set()
            
        if task in visited:
            return []
            
        visited.add(task)
        current_path = path + [task.name]
        
        dependents = reverse_map[task]
        if not dependents:
            return [current_path]
            
        all_paths = []
        for dependent in dependents:
            dependent_paths = trace_path(dependent, current_path, visited.copy())
            all_paths.extend(dependent_paths)
            
        return all_paths
    
    all_execution_paths = []
    for root_task in root_tasks:
        paths = trace_path(root_task)
        all_execution_paths.extend(paths)
    
    for i, path in enumerate(all_execution_paths, 1):
        print(f"  Path {i}: {' → '.join(path)}")
    
    print("\n=== END OF SUMMARY ===")


class CircularDependencyError(Exception):
    """Exception raised when a circular dependency is detected in the task graph."""
    def __init__(self, cycle):
        self.cycle = cycle
        cycle_str = " → ".join([task.name for task in cycle])
        super().__init__(f"Circular dependency detected: {cycle_str}")

def detect_circular_dependencies(tasks):
    """
    Detects circular dependencies in the task graph using DFS.
    
    Args:
        tasks: List of Task objects
    
    Returns:
        List of cycles found in the graph, where each cycle is a list of Task objects
    
    Raises:
        CircularDependencyError: If a circular dependency is detected
    """
    # Build dependency map
    dependency_map = {}
    for task in tasks:
        dependencies = []
        # Check args for dependencies
        for binding in task.fn_args:
            dependencies.append(binding.source)
        # Check kwargs for dependencies
        for binding in task.fn_kwargs.values():
            dependencies.append(binding.source)
        dependency_map[task] = dependencies
    
    # Track visited nodes and current path
    visited = set()
    path = []
    path_set = set()
    cycles = []
    
    def dfs(node):
        if node in path_set:
            # Found a cycle
            cycle_start_idx = path.index(node)
            cycle = path[cycle_start_idx:] + [node]
            cycles.append(cycle)
            return
        
        if node in visited:
            return
            
        visited.add(node)
        path.append(node)
        path_set.add(node)
        
        for dep in dependency_map.get(node, []):
            dfs(dep)
            
        path.pop()
        path_set.remove(node)
    
    # Run DFS from each node
    for task in tasks:
        dfs(task)
    
    if cycles:
        print('circular dependency detected. cycles:', cycles)
        # Raise exception with the first cycle found
        raise CircularDependencyError(cycles[0])
    
    return cycles






def mark_tasks_whose_dependencies_are_satisfied_as_ready(tasks):
    """Marks tasks whose dependencies are satisfied as ready."""
    for task in tasks:
        if task.ready:
            continue
        task.ready = all(binding.source.completed for binding in flatten(task.fn_args + list(task.fn_kwargs.values())))

def make_runner(task):
    """Makes a runner for a task."""
    def runner():
        return task.fn(*task.fn_args, **task.fn_kwargs)
    return runner

def run_graph(tasks):
    detect_circular_dependencies(tasks)
    print('no circular dependency detected')
    print_task_graph_summary(tasks)
    
    
    with ThreadPoolExecutor() as executor:
        future_to_task = {}
        
        def run_ready_tasks():
            for task in filter(lambda t: t.ready and t.num_runs==0, tasks):
                task.resolve_bindings()
                runner = make_runner(task)
                new_future = executor.submit(runner)
                task.num_runs += 1
                future_to_task[new_future] = task
        
        run_ready_tasks()
        
        while future_to_task:
            for future in as_completed(future_to_task): # Wait for the next completed future
                task = future_to_task.pop(future)
                task.output = future.result()
                task.completed = True
                mark_tasks_whose_dependencies_are_satisfied_as_ready(tasks)
                run_ready_tasks()
                if task.yielder:
                    yield task.output, task.name
                    

for x in run_graph(tasks):
    print(x)



