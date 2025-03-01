from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

def run_command(cmd):
    """Runs a command and returns its stdout output."""
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return cmd, result.stdout.strip(), result.stderr.strip()

# Initial commands with dependencies
# Format: [command, [list of dependency indices]]
commands_with_deps = [
    [["echo", "Hello, World!"], []],  # No dependencies
    [["ls", "-l"], []],  # No dependencies
    [["uname", "-a"], []],  # No dependencies
    [["echo", "This runs after Hello World"], [0]],  # Depends on command 0
    [["echo", "This runs after ls and uname"], [1, 2]],  # Depends on commands 1 and 2
    [["echo", "Final command - runs after everything"], [3, 4]]  # Depends on commands 3 and 4
]

# Track completed commands and their results
completed_commands = set()
command_results = {}

# Commands ready to be executed (those with no dependencies initially)
ready_commands = [cmd_info for idx, cmd_info in enumerate(commands_with_deps) if not cmd_info[1]]

# Run commands in parallel with dependency management
with ThreadPoolExecutor() as executor:
    # Start with initial batch of commands that have no dependencies
    future_to_cmd_idx = {}
    for cmd_info in ready_commands:
        cmd = cmd_info[0]
        # Find the index of this command in the original list
        cmd_idx = commands_with_deps.index(cmd_info)
        future = executor.submit(run_command, cmd)
        future_to_cmd_idx[future] = cmd_idx
    
    # Process results and submit new commands based on dependencies
    while future_to_cmd_idx:
        # Wait for the next completed future
        for future in as_completed(future_to_cmd_idx):
            cmd_idx = future_to_cmd_idx.pop(future)
            cmd, stdout, stderr = future.result()
            
            print(f"Command: {' '.join(cmd)}")
            print(f"Output:\n{stdout}")
            if stderr:
                print(f"Error:\n{stderr}")
            print("-" * 40)
            
            # Mark this command as completed
            completed_commands.add(cmd_idx)
            command_results[cmd_idx] = (stdout, stderr)
            
            # Check if any pending commands can now be executed
            for idx, (cmd, deps) in enumerate(commands_with_deps):
                if idx not in completed_commands and idx not in [future_to_cmd_idx[f] for f in future_to_cmd_idx]:
                    # Check if all dependencies are satisfied
                    if all(dep in completed_commands for dep in deps):
                        # Submit this command
                        new_future = executor.submit(run_command, cmd)
                        future_to_cmd_idx[new_future] = idx
            
            # Only process one completed future at a time
            break