# inspired from https://github.com/ParthS007/background
import multiprocessing # can be used to get cpu count later
import concurrent.futures

class Background:
    def __init__(self, n=10):
        self.n = n
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=n)
        self.callbacks = []
        self.results = []

    def run(self, f, *args, **kwargs):
        self.pool._max_workers = self.n
        self.pool._adjust_thread_count()
        future = self.pool.submit(f, *args, **kwargs)
        future.source_function = f.__name__
        self.results.append(future)
        return future

    def task(self, f):
        def do_task(*args, **kwargs):
            result = self.run(f, *args, **kwargs)
            for cb in self.callbacks:
                result.add_done_callback(cb)
            return result
        return do_task

    def callback(self, f):
        self.callbacks.append(f)
        def register_callback():
            f()
        return register_callback


'''
Example usage here
'''
if __name__ == "__main__":
    import time

    background = Background(n=40)

    @background.task
    def work():
        time.sleep(3)
        return "Done!"
    
    @background.task
    def hello():
        time.sleep(2)
        return "Hello!"

    @background.callback
    def work_callback(future):
        print('from', future.source_function, 'received', future.result(),'\n\n')
        
    work()
    work()
    hello()
    hello()