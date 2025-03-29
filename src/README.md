# PyToolkit Test Framework

A modular and extensible testing framework for performance, replay, and recovery testing.

## Architecture Overview

The framework uses several design patterns to provide a flexible and maintainable testing solution:
- Factory Pattern: For creating different types of tests
- Strategy Pattern: For executing different test strategies
- Registry Pattern: For registering new test types
- Facade Pattern: For providing a simplified interface to the test system

### Core Components

1. **Test Factory** (`test_factory.py`)
   - Manages test type registration
   - Creates test instances
   - Provides base test interface

2. **Test Stages** (`stages.py`)
   - Defines individual test steps
   - Manages stage execution
   - Contains pre-defined stage collections

3. **Test Suites** (`test_suites.py`)
   - Creates test suites from stages
   - Manages test execution
   - Handles results and reporting

4. **Metrics** (`metrics.py`)
   - Calculates performance metrics
   - Processes test results
   - Generates statistical analysis

5. **Graphs** (`graph.py`)
   - Creates visualization of test results
   - Generates scatter plots and multi-plots
   - Saves plots to files

## Adding New Components

### 1. Adding a New Stage

Create a new stage function in `stages.py`:

```python
def new_custom_stage(input_data):
    print(f"Executing custom stage with: {input_data}")
    return {
        "status": "success",
        "result": "custom_result"
    }
```

Add the stage to a test collection:

```python
def get_custom_test_stages():
    return [
        Stage("connect", connect_stage),
        Stage("custom", new_custom_stage),
        Stage("calculate_metrics", calculate_metrics_stage),
        Stage("create_graphs", create_graphs_stage),
    ]
```

### 2. Adding a New Test Type

1. Create a new test class in test_factory.py:

```python
class CustomTest(Test):
    def run(self, app_name: str, stages: List[Stage], **kwargs):
        results = {}
        for stage in stages:
            results[stage.name] = stage.execute(
                app_name if stage.name == "connect"
                else kwargs.get('custom_data') if stage.name == "custom"
                else results
            )
        return results
```

2. Register the test type:

```python
# In test_factory.py
TestFactory.register("custom", CustomTest)
```

3. Create an execution strategy in test_suites.py

```python
class CustomExecutionStrategy(TestExecutionStrategy):
    def execute(self, test, app_name: str, stages: List[Stage]) -> Dict[str, Any]:
        return test.run(
            app_name,
            stages,
            custom_data={"key": "value"}
        )

# Register the strategy
TestExecutionFactory.register_strategy("custom", CustomExecutionStrategy())

```

### 3. Using the New Test Type

```python
# In your test script
facade = AppTestFacade()

# Register app with custom stages
facade.register_app("MyApp", {
    "custom": get_custom_test_stages(),
})

# Run tests
facade.run_all_tests()
```

### Test Flow

1. **Registration**: Tests are registered with the TestFactory
2. **Stage Definition**: Stages are defined and organized into collections
3. **Execution**: Tests are executed through the facade
4. **Results Processing**: Results are collected and processed
5. **Visualization**: Metrics are calculated and graphs are generated

### Example: Complete Test Flow

```python
from testplan import Testplan
from test_factory import TestFactory, Test
from stages import Stage, get_custom_test_stages

# 1. Define new test type
class CustomTest(Test):
    def run(self, app_name: str, stages: List[Stage], **kwargs):
        results = {}
        for stage in stages:
            results[stage.name] = stage.execute(
                app_name if stage.name == "connect"
                else kwargs.get('custom_data') if stage.name == "custom"
                else results
            )
        return results

# 2. Register test type
TestFactory.register("custom", CustomTest)

# 3. Create test facade instance
facade = AppTestFacade()

# 4. Register app with test stages
facade.register_app("MyApp", {
    "custom": get_custom_test_stages(),
})

# 5. Run tests
facade.run_all_tests()
```

### Output Directory Structure

```text
pytoolkit/
├── graphs/
│   ├── response_times_20240328_220613.png
│   └── response_time_analysis_20240328_220613.png
├── test_factory.py
├── stages.py
├── test_suites.py
├── metrics.py
└── graph.py
```

### Best Practices

#### Stage Design

- Keep stages focused on a single responsibility

- Ensure proper error handling

- Return structured results

#### Test Implementation

- Inherit from the base Test class

- Implement the required run method

- Handle all required parameters

#### Results Processing

- Include status information

- Provide detailed error messages

- Format results consistently

#### Error Handling

- Use try-except blocks appropriately

- Provide meaningful error messages

- Clean up resources in finally blocks

### Dependencies

- Python 3.7+

- numpy

- matplotlib

- testplan

### Installation

```bash
pip install numpy matplotlib testplan
```

### Running Tests

```bash
python test_plan_performance.py
```

### Contributing

1. Follow the existing patterns for new components

2. Add appropriate error handling

3. Update tests for new functionality

4. Document new features and changes

### License

#### MIT License
