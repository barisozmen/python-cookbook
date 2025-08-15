from task import Task, Binding
from run import run_graph
import time

def make_generate_data_stream(count):
    def generate_data_stream():
        """A function that generates data incrementally"""
        for i in range(count):
            time.sleep(0.5)  # Simulate work being done
            yield f"Data chunk {i+1}"
            print(f"Generated chunk {i+1}")
    return generate_data_stream

def process_data(data):
    """Process the data received"""
    return f"Processed: {data}"

def main():
    # Create tasks
    stream_task = Task(
        name="data_stream",
        fn=make_generate_data_stream(5),
        yielder=True,
        ready=True,
    )
    
    process_task = Task(
        name="process_data",
        fn=process_data,
        fn_args=[Binding(stream_task)],  # This task depends on stream_task
        yielder=True,
    )
    
    # Run the graph and process streaming results
    for result, task_name in run_graph([stream_task, process_task]):
        if ":partial" in task_name:
            print(f"Received partial result from {task_name.split(':')[0]}: {result}")
        else:
            print(f"Received final result from {task_name}: {result}")

if __name__ == "__main__":
    main()