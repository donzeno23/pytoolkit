# stages.py

import random
from typing import Any, Callable
from metrics import MetricsCalculator
from graph import ResponseTimeGrapher

class Stage:
    def __init__(self, name: str, action: Callable[..., Any]):
        self.name = name
        self.action = action

    def execute(self, *args, **kwargs):
        return self.action(*args, **kwargs)

# Stage action definitions
def connect_stage(app_name):
    print(f"Connecting to {app_name}...")
    return True

def get_log_stage(app_name):
    print(f"Getting log from {app_name}...")
    return "dummy_log.txt"

def inject_data_stage(batch_data):
    print(f"Injecting data: {batch_data}")
    return {"status": "success"}

# def read_log_stage(log_path):
#     print(f"Reading log from {log_path}...")
#     return ["Log entry 1", "Log entry 2"]
def read_log_stage(log_path):
    print(f"Reading log from {log_path}...")
    # Simulate response times from log
    response_times = [random.uniform(0.1, 0.5) for _ in range(100)]
    return {
        "status": "success",
        "response_times": response_times,
        "entries": ["Log entry 1", "Log entry 2"]
    }

# def send_batch_stage(batch_data):
#     print(f"Sending batch: {batch_data}")
#     return {"status": "success"}
def send_batch_stage(batch_data):
    print(f"Sending batch: {batch_data}")
    # Simulate response times for batch operations
    response_times = [random.uniform(0.1, 0.5) for _ in range(100)]
    return {
        "status": "success",
        "response_times": response_times,
        "batch_size": len(batch_data.get("data", []))
    }

# def calculate_metrics_stage(results):
#     print(f"Calculating metrics from {results}...")
#     return {"average": 10.5, "max": 20}
'''
def calculate_metrics_stage(results: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate performance metrics from test results.
    
    Args:
        results: Dictionary containing test results, expected to have
                'response_times' key with list of numerical values
                
    Returns:
        Dictionary containing calculated metrics
        
    Raises:
        ValueError: If required data is missing or invalid
    """
    print(f"Calculating metrics from {results}...")
    
    # Extract response times from results
    response_times = results.get('send_batch', {}).get('response_times')
    if not response_times:
        raise ValueError("No response times found in results")

    try:
        # Calculate metrics using MetricsCalculator
        metrics = MetricsCalculator.process_metrics(response_times)
        
        return {
            "metrics": metrics,
            "status": "success",
            "sample_size": len(response_times)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
'''
def calculate_metrics_stage(results: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate performance metrics from test results.
    
    Args:
        results: Dictionary containing test results, expected to have
                'response_times' key with list of numerical values
                
    Returns:
        Dictionary containing calculated metrics
        
    Raises:
        ValueError: If required data is missing or invalid
    """
    print(f"Calculating metrics from {results}...")
    
    # Extract response times from either send_batch or read_log results
    response_times = None
    for stage_name in ['send_batch', 'read_log']:
        if stage_name in results:
            response_times = results[stage_name].get('response_times')
            if response_times:
                break

    if not response_times:
        raise ValueError("No response times found in results")

    try:
        # Calculate metrics using MetricsCalculator
        metrics = MetricsCalculator.process_metrics(response_times)
        
        return {
            "metrics": metrics,
            "status": "success",
            "sample_size": len(response_times),
            "source": "send_batch" if "send_batch" in results else "read_log",
            "response_times": response_times # Pass response times to next stage
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def create_graphs_stage(results: dict[str, Any]) -> dict[str, Any]:
    """
    Create performance graphs from test results.
    
    Args:
        results: Dictionary containing test results and metrics
                
    Returns:
        Dictionary containing paths to generated graphs
        
    Raises:
        ValueError: If required data is missing
    """
    print("Generating performance graphs...")

    # Get response times from previous stage results
    metrics_result = results.get('calculate_metrics', {})
    response_times = metrics_result.get('response_times')
    source = metrics_result.get('source', 'unknown')

    if not response_times:
        raise ValueError("No response times found in metrics results")

    try:
        grapher = ResponseTimeGrapher()
        
        # Create scatter plot
        scatter_plot_path = grapher.create_scatter_plot(
            response_times,
            title=f"Response Times Over Time - {source.replace('_', ' ').title()}"
        )
        
        # Create multi-plot analysis
        analysis_plot_path = grapher.create_multi_plot(
            response_times,
            title=f"Response Time Analysis - {source.replace('_', ' ').title()}"
        )
        
        return {
            "status": "success",
            "graphs": {
                "scatter_plot": scatter_plot_path,
                "analysis_plot": analysis_plot_path
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# Pre-defined stage collections
def get_replay_stages():
    return [
        Stage("connect", connect_stage),
        Stage("get_log", get_log_stage),
        Stage("inject_data", inject_data_stage),
    ]

def get_performance_stages():
    return [
        Stage("connect", connect_stage),
        Stage("send_batch", send_batch_stage),
        Stage("calculate_metrics", calculate_metrics_stage),
        Stage("create_graphs", create_graphs_stage)
    ]

def get_recovery_stages():
    return [
        Stage("connect", connect_stage),
        Stage("read_log", read_log_stage),
        Stage("calculate_metrics", calculate_metrics_stage),
        Stage("create_graphs", create_graphs_stage)
    ]