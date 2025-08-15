from task import Task, Binding, make_identity
from run import run_graph
from tasteful import delegator
from datetime import datetime
from functools import wraps


def current_time_human_readable():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def timer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = current_time_human_readable()
        res = fn(*args, **kwargs)
        end = current_time_human_readable()
        print(f'{fn.__name__} started at {start} and ended at {end}')
        return res
    return wrapper


def make_llm_fn(prompt):
    @timer
    def fn():
        c = delegator.run(f'baris plain {prompt}')
        return c.out
    return fn

@timer
def merger_llm(compiler_design, lisp, computer_scientists):
    
    cmd = (
        f'baris plain "Think yourself of one of the CS people among: '
        f'{computer_scientists}\n\n'
        'And answer the following questions one by one:\n'
        f'{compiler_design}\n\n'
        f'{lisp}\n\n"'
    )
    print('merger_llm command is:', cmd)
    c = delegator.run(cmd)
    return c.out

compiler_design = Task(
    make_llm_fn('Ask me three questions about Compiler Design. Give only the questions, no answers, and say nothing else.'),
    ready=True,
    yielder=True,
)
lisp = Task(
    make_llm_fn('Ask me three questions about Lisp language. Give only the questions, no answers, and say nothing else.'),
    ready=True,
    yielder=True,
)
computer_scientists = Task(
    make_llm_fn('Tell me the biggest computer scientists of all time. Give only the names, and say nothing else.'),
    ready=True,
    yielder=True,
)

final = Task(
    merger_llm,
    fn_kwargs={'compiler_design': Binding(compiler_design), 'lisp': Binding(lisp), 'computer_scientists': Binding(computer_scientists)},
    yielder=True,
)

for k, v in locals().copy().items():
    if isinstance(v, Task):
        v.name = k
tasks = [v for v in locals().copy().values() if isinstance(v, Task)]



for x in run_graph(tasks):
    print(x)