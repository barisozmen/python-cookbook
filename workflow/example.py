from task import Task, Binding, make_identity
from run import run_graph


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



for x in run_graph(tasks):
    print(x)