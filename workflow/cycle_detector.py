

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














##### TESTS #####


import unittest
from unittest.mock import patch, MagicMock


from task import Task, Binding

class TestDetectCircularDependencies(unittest.TestCase):
    
    def setUp(self):
        # Create mock functions for tasks
        self.fn1 = lambda: "Task 1"
        self.fn2 = lambda: "Task 2"
        self.fn3 = lambda: "Task 3"
        self.fn4 = lambda: "Task 4"
    
    def test_no_dependencies(self):
        # Test with tasks that have no dependencies
        task1 = Task(self.fn1, name="task1", ready=True)
        task2 = Task(self.fn2, name="task2", ready=True)
        
        tasks = [task1, task2]
        
        # Should not detect any cycles
        cycles = detect_circular_dependencies(tasks)
        self.assertEqual(cycles, [])
    
    def test_linear_dependencies(self):
        # Test with linear dependencies (no cycles)
        task1 = Task(self.fn1, name="task1", ready=True)
        task2 = Task(self.fn2, name="task2", fn_args=[Binding(task1)])
        task3 = Task(self.fn3, name="task3", fn_args=[Binding(task2)])
        
        tasks = [task1, task2, task3]
        
        # Should not detect any cycles
        cycles = detect_circular_dependencies(tasks)
        self.assertEqual(cycles, [])
    
    def test_diamond_dependencies(self):
        # Test with diamond-shaped dependencies (no cycles)
        task1 = Task(self.fn1, name="task1", ready=True)
        task2 = Task(self.fn2, name="task2", fn_args=[Binding(task1)])
        task3 = Task(self.fn3, name="task3", fn_args=[Binding(task1)])
        task4 = Task(self.fn4, name="task4", fn_args=[Binding(task2), Binding(task3)])
        
        tasks = [task1, task2, task3, task4]
        
        # Should not detect any cycles
        cycles = detect_circular_dependencies(tasks)
        self.assertEqual(cycles, [])
    
    def test_simple_cycle(self):
        # Test with a simple cycle: task1 -> task2 -> task1
        task1 = Task(self.fn1, name="task1")
        task2 = Task(self.fn2, name="task2")
        
        # Create circular dependency
        task1.fn_args = [Binding(task2)]
        task2.fn_args = [Binding(task1)]
        
        tasks = [task1, task2]
        
        # Should raise CircularDependencyError
        with self.assertRaises(CircularDependencyError) as context:
            detect_circular_dependencies(tasks)
        
        # Verify the cycle in the exception
        self.assertIn("task1", str(context.exception))
        self.assertIn("task2", str(context.exception))
    
    def test_complex_cycle(self):
        # Test with a more complex cycle: task1 -> task2 -> task3 -> task1
        task1 = Task(self.fn1, name="task1")
        task2 = Task(self.fn2, name="task2")
        task3 = Task(self.fn3, name="task3")
        
        # Create circular dependency
        task1.fn_args = [Binding(task3)]
        task2.fn_args = [Binding(task1)]
        task3.fn_args = [Binding(task2)]
        
        tasks = [task1, task2, task3]
        
        # Should raise CircularDependencyError
        with self.assertRaises(CircularDependencyError) as context:
            detect_circular_dependencies(tasks)
        
        # Verify the cycle in the exception
        exception_msg = str(context.exception)
        self.assertTrue(
            "task1 → task2 → task3 → task1" in exception_msg or
            "task2 → task3 → task1 → task2" in exception_msg or
            "task3 → task1 → task2 → task3" in exception_msg or
            "task1 → task3 → task2 → task1" in exception_msg
        )
    
    def test_cycle_with_kwargs(self):
        # Test with a cycle involving kwargs
        task1 = Task(self.fn1, name="task1")
        task2 = Task(self.fn2, name="task2")
        
        # Create circular dependency using kwargs
        task1.fn_kwargs = {"param": Binding(task2)}
        task2.fn_args = [Binding(task1)]
        
        tasks = [task1, task2]
        
        # Should raise CircularDependencyError
        with self.assertRaises(CircularDependencyError):
            detect_circular_dependencies(tasks)
    
    def test_multiple_cycles(self):
        # Test with multiple cycles in the graph
        task1 = Task(self.fn1, name="task1")
        task2 = Task(self.fn2, name="task2")
        task3 = Task(self.fn3, name="task3")
        task4 = Task(self.fn4, name="task4")
        
        # Create two cycles: task1 <-> task2 and task3 <-> task4
        task1.fn_args = [Binding(task2)]
        task2.fn_args = [Binding(task1)]
        task3.fn_args = [Binding(task4)]
        task4.fn_args = [Binding(task3)]
        
        tasks = [task1, task2, task3, task4]
        
        # Should raise CircularDependencyError for the first cycle found
        with self.assertRaises(CircularDependencyError):
            detect_circular_dependencies(tasks)
    
    @patch('builtins.print')
    def test_print_message_on_cycle_detection(self, mock_print):
        # Test that the function prints a message when a cycle is detected
        task1 = Task(self.fn1, name="task1")
        task2 = Task(self.fn2, name="task2")
        
        # Create circular dependency
        task1.fn_args = [Binding(task2)]
        task2.fn_args = [Binding(task1)]
        
        tasks = [task1, task2]
        
        # Should raise CircularDependencyError
        with self.assertRaises(CircularDependencyError):
            detect_circular_dependencies(tasks)
        
        # Verify that print was called with the expected message
        mock_print.assert_called_once()
        self.assertIn('circular dependency detected', mock_print.call_args[0][0])

if __name__ == '__main__':
    unittest.main()