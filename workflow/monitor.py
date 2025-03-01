
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