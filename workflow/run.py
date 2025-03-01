from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))


from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import flatten

from monitor import print_task_graph_summary
from cycle_detector import detect_circular_dependencies
  

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

def run_graph(tasks, max_workers=10):
    detect_circular_dependencies(tasks)
    print('no circular dependency detected')
    print_task_graph_summary(tasks)
    
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
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





