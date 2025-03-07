# Code Execution Optimization

## Overview
The current implementation of code execution in tools.py is inefficient, using fixed timeouts regardless of code complexity and employing a basic thread execution model. This plan outlines improvements to make code execution more efficient and secure.

## Problem
- Fixed timeouts regardless of code complexity
- Inefficient resource usage during execution
- No caching of execution results for similar code
- Limited output handling and truncation
- Basic error handling
- Simple security checks that could be bypassed

## Solution
Implement a more sophisticated code execution system:
1. Create a dedicated CodeExecutor class with resource monitoring
2. Add caching for repeated code executions
3. Implement adaptive timeouts based on code complexity
4. Enhance security through sandboxing and better code verification
5. Improve output handling and formatting

## Implementation Steps

### 1. Create a Dedicated CodeExecutor Class
```python
import io
import sys
import time
import hashlib
import threading
import traceback
import concurrent.futures
import ast
import re
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

class CodeExecutor:
    def __init__(self, cache_size=100, default_timeout=60, max_output_len=10000):
        """Initialize the code executor with cache"""
        self.cache = {}  # Cache for execution results
        self.cache_size = cache_size
        self.default_timeout = default_timeout
        self.max_output_len = max_output_len
        self.lock = threading.Lock()
        
    def _hash_code(self, code_str):
        """Create a hash of the code string for caching"""
        return hashlib.md5(code_str.encode('utf-8')).hexdigest()
        
    def _estimate_complexity(self, code_str):
        """Estimate code complexity to determine appropriate timeout"""
        # Start with default timeout
        timeout = self.default_timeout
        
        try:
            # Parse the code to AST
            tree = ast.parse(code_str)
            
            # Count loops and function calls
            loop_count = 0
            call_count = 0
            
            # Simple visitor to count loops and calls
            for node in ast.walk(tree):
                if isinstance(node, (ast.For, ast.While)):
                    loop_count += 1
                elif isinstance(node, ast.Call):
                    call_count += 1
            
            # Adjust timeout based on complexity
            timeout = min(300, self.default_timeout + (loop_count * 10) + (call_count * 2))
            
            # Check for specific performance-intensive operations
            if "load_dataset" in code_str:
                timeout = min(300, timeout * 2)  # Data loading needs more time
            if "train" in code_str and ("model" in code_str or "fit" in code_str):
                timeout = min(300, timeout * 3)  # Model training needs more time
                
        except SyntaxError:
            # If code can't be parsed, use default timeout
            pass
            
        return timeout
    
    def _check_security(self, code_str):
        """Check code for security issues"""
        # List of banned patterns
        banned_patterns = [
            r'os\s*\.\s*system',
            r'subprocess',
            r'exec\s*\(',
            r'eval\s*\(',
            r'__import__\s*\(',
            r'open\s*\([^)]*,\s*[\'"]w[\'"]\)',
            r'socket\.',
            r'requests\.delete',
            r'requests\.put',
            r'requests\.post',
            r'\.delete\(',
            r'\.destroy\(',
            r'shutil\.rmtree',
            r'exit\(',
            r'quit\(',
            r'sys\.exit',
            r'rm\s+-rf',
        ]
        
        for pattern in banned_patterns:
            if re.search(pattern, code_str):
                return False, f"Blocked potentially harmful code pattern: {pattern}"
                
        return True, ""
    
    def _run_code(self, code_str):
        """Execute code and capture output"""
        # Redirect stdout
        output_capture = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output_capture
        
        result = None
        error = None
        
        try:
            # Create a clean namespace
            exec_globals = {}
            
            # Add safe imports
            safe_modules = {
                'numpy': 'np',
                'pandas': 'pd',
                'matplotlib.pyplot': 'plt',
                'sklearn': 'sklearn',
                'torch': 'torch',
                'tensorflow': 'tf'
            }
            
            for module, alias in safe_modules.items():
                try:
                    exec(f"import {module} as {alias}", exec_globals)
                except ImportError:
                    pass
            
            # Execute the code
            exec(code_str, exec_globals)
            
            # Check if the code created a figure and save it
            if 'plt' in exec_globals and plt.get_fignums():
                plt.savefig('output_figure.png')
                output_capture.write("[Figure saved as output_figure.png]\n")
                plt.close()
                
            result = output_capture.getvalue()
            
        except Exception as e:
            error = f"[CODE EXECUTION ERROR]: {str(e)}\n{traceback.format_exc()}"
            
        finally:
            # Restore stdout
            sys.stdout = original_stdout
            
        return result, error
    
    def execute(self, code_str, timeout=None):
        """Execute code with timeout and caching"""
        # First, check security
        is_safe, security_message = self._check_security(code_str)
        if not is_safe:
            return security_message
            
        # Normalize code (remove whitespace variations)
        code_str = '\n'.join(line.rstrip() for line in code_str.splitlines())
        
        # Check cache
        code_hash = self._hash_code(code_str)
        with self.lock:
            if code_hash in self.cache:
                return self.cache[code_hash]
                
        # Determine timeout
        if timeout is None:
            timeout = self._estimate_complexity(code_str)
            
        # Execute with timeout
        output = None
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self._run_code, code_str)
            try:
                result, error = future.result(timeout=timeout)
                if error:
                    output = error
                else:
                    output = result if result else "[No output]"
            except concurrent.futures.TimeoutError:
                output = f"[CODE EXECUTION ERROR]: Code execution exceeded the timeout limit of {timeout} seconds. You must reduce the time complexity of your code."
                
        # Truncate output if too long
        if len(output) > self.max_output_len:
            output = output[:self.max_output_len] + f"\n[Output truncated, exceeded {self.max_output_len} characters]"
            
        # Cache the result
        with self.lock:
            if len(self.cache) >= self.cache_size:
                # Remove oldest entry (first key)
                self.cache.pop(next(iter(self.cache)))
            self.cache[code_hash] = output
            
        return output
```

### 2. Update the execute_code Function
```python
# In tools.py

# Create a singleton executor instance
_code_executor = CodeExecutor()

def execute_code(code_str, timeout=60, MAX_LEN=10000):
    """Execute code with the optimized executor"""
    # Prevent unsafe operations
    if "load_dataset('pubmed" in code_str:
        return "[CODE EXECUTION ERROR] pubmed Download took way too long. Program terminated"
    if "exit(" in code_str or "quit(" in code_str or "sys.exit" in code_str:
        return "[CODE EXECUTION ERROR] Exit commands are not allowed"
        
    # Run the code with the executor
    return _code_executor.execute(code_str, timeout)
```

### 3. Add a Batch Code Execution Method
```python
def execute_code_batch(code_segments, timeout=60):
    """Execute multiple code segments in sequence
    
    Args:
        code_segments (list): List of code strings to execute
        timeout (int): Timeout for each segment
        
    Returns:
        list: Results for each code segment
    """
    results = []
    
    # Create environment variables to share context between segments
    env_vars = {}
    
    for i, code in enumerate(code_segments):
        # Wrap code to capture variables
        wrapped_code = f"""
# Import environment from previous segments
globals().update({env_vars})

# Execute the current segment
{code}

# Save environment for next segment
_env_capture = {{k: v for k, v in globals().items() 
               if not k.startswith('_') and k != 'env_vars'}}
"""
        # Execute the segment
        result = _code_executor.execute(wrapped_code, timeout)
        results.append(result)
        
        # Update environment if not an error
        if not result.startswith("[CODE EXECUTION ERROR]"):
            try:
                # Extract the captured environment
                env_vars = eval('_env_capture', globals())
            except:
                pass
                
    return results
```

### 4. Implement Resource Monitoring
```python
import psutil
import os

class ResourceMonitor:
    """Monitor and limit resource usage during code execution"""
    
    def __init__(self, memory_limit_mb=1000, cpu_percent_limit=80):
        self.memory_limit = memory_limit_mb * 1024 * 1024  # Convert to bytes
        self.cpu_percent_limit = cpu_percent_limit
        self.process = psutil.Process(os.getpid())
        
    def check_resources(self):
        """Check if resource usage is within limits
        
        Returns:
            tuple: (is_within_limits, message)
        """
        # Check memory usage
        memory_info = self.process.memory_info()
        if memory_info.rss > self.memory_limit:
            return (False, f"Memory usage exceeded limit: {memory_info.rss / (1024*1024):.1f}MB > {self.memory_limit / (1024*1024)}MB")
            
        # Check CPU usage
        cpu_percent = self.process.cpu_percent(interval=0.1)
        if cpu_percent > self.cpu_percent_limit:
            return (False, f"CPU usage exceeded limit: {cpu_percent:.1f}% > {self.cpu_percent_limit}%")
            
        return (True, "")
        
    def monitor_execution(self, func, *args, **kwargs):
        """Run a function while monitoring resource usage"""
        result_queue = queue.Queue()
        stop_event = threading.Event()
        
        def _monitor():
            while not stop_event.is_set():
                is_ok, message = self.check_resources()
                if not is_ok:
                    result_queue.put(("ERROR", message))
                    return
                time.sleep(0.5)
                
        def _run_func():
            try:
                result = func(*args, **kwargs)
                result_queue.put(("RESULT", result))
            except Exception as e:
                result_queue.put(("ERROR", str(e)))
                
        # Start monitoring thread
        monitor_thread = threading.Thread(target=_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Start function thread
        func_thread = threading.Thread(target=_run_func)
        func_thread.daemon = True
        func_thread.start()
        
        # Wait for result or timeout
        try:
            result_type, result = result_queue.get(timeout=60)
            stop_event.set()
            
            if result_type == "ERROR":
                return f"[RESOURCE ERROR]: {result}"
            else:
                return result
        except queue.Empty:
            stop_event.set()
            return "[TIMEOUT ERROR]: Execution took too long"
```

### 5. Add to CodeExecutor Class to Use Resource Monitoring
```python
# Enhance the _run_code method in CodeExecutor
def _run_code(self, code_str):
    """Execute code with resource monitoring"""
    # Create resource monitor
    monitor = ResourceMonitor()
    
    # Define the execution function
    def _execute():
        # (original _run_code implementation)
        ...
        
    # Run with monitoring
    return monitor.monitor_execution(_execute)
```

## Benefits
- More efficient resource usage during code execution
- Adaptive timeouts based on code complexity
- Reduced redundant executions through caching
- Enhanced security through better code verification
- Improved output handling and formatting
- Better error messages and debugging information

## Metrics for Success
- 40%+ reduction in execution time for cached code segments
- More appropriate timeouts based on code complexity
- Zero security vulnerabilities in code execution
- Improved output readability with proper figure handling
- Better context preservation between code segments