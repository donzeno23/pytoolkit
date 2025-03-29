# test_suites.py

from testplan.testing.multitest import testsuite, testcase
from typing import List, Dict, Any
import random
from abc import ABC, abstractmethod

from stages import Stage
from test_factory import TestFactory, register_test

def generate_name(func_name, kwargs):
    """Custom name generator for parametrized testcases"""
    random_num = random.random()
    return f"{func_name}_{random_num}"

# Strategy Pattern for test execution
class TestExecutionStrategy(ABC):
    @abstractmethod
    def execute(self, test, app_name: str, stages: List[Stage]) -> Dict[str, Any]:
        pass

# @register_test("replay")
class ReplayExecutionStrategy(TestExecutionStrategy):
    def execute(self, test, app_name: str, stages: List[Stage]) -> Dict[str, Any]:
        return test.run(
            app_name,
            stages,
            log_path="app.log",
            batch_data={"data": [1, 2, 3]}
        )

# @register_test("performance")
class PerformanceExecutionStrategy(TestExecutionStrategy):
    def execute(self, test, app_name: str, stages: List[Stage]) -> Dict[str, Any]:
        return test.run(
            app_name,
            stages,
            batch_data={"data": [1, 2, 3]}
        )

# @register_test("recovery")
class RecoveryExecutionStrategy(TestExecutionStrategy):
    def execute(self, test, app_name: str, stages: List[Stage]) -> Dict[str, Any]:
        return test.run(
            app_name,
            stages
        )

class TestExecutionFactory:
    _strategies: Dict[str, TestExecutionStrategy] = {}

    @classmethod
    def register_strategy(cls, test_type: str, strategy: TestExecutionStrategy) -> None:
        cls._strategies[test_type] = strategy

    @classmethod
    def get_strategy(cls, test_type: str) -> TestExecutionStrategy:
        strategy = cls._strategies.get(test_type)
        if not strategy:
            raise ValueError(f"No execution strategy found for test type: {test_type}")
        return strategy

# Register execution strategies
TestExecutionFactory.register_strategy("replay", ReplayExecutionStrategy())
TestExecutionFactory.register_strategy("performance", PerformanceExecutionStrategy())
TestExecutionFactory.register_strategy("recovery", RecoveryExecutionStrategy())

def create_test_suite(test_type: str, stages: list[Stage], app_name: str):
    """Factory function to create a configured test suite"""
    
    @testsuite(name=f"{test_type.capitalize()}TestSuite")
    class CustomTestSuite:
        def __init__(self):
            self.test_factory = TestFactory()
            self.test_type = test_type
            self.stages = stages
            self.app_name = app_name
            self.execution_strategy = TestExecutionFactory.get_strategy(test_type)

        @testcase(name_func=generate_name)
        def test_case(self, env, result):
            print(f"\n=== Running {self.test_type.upper()} Test ===")

            try:
                # Create test instance using registry-based factory
                test = self.test_factory.create_test(self.test_type)
                
                # Execute test using appropriate strategy
                test_result = self.execution_strategy.execute(
                    test,
                    self.app_name,
                    self.stages
                )

                # Log results
                result.log(f"\nExecuting {self.test_type.upper()} test for {self.app_name}")
                result.log(f"Test '{self.test_type.upper()}' completed with result: {test_result}")
                
                # Print stage results
                print(f"\nStage Results for {self.test_type.upper()}:")
                for stage in self.stages:
                    stage_result = test_result.get(stage.name, 'N/A')
                    print(f"  - Stage '{stage.name}': {stage_result}")
                    result.log(f"Stage '{stage.name}' result: {stage_result}")
                
            except Exception as e:
                error_msg = f"Error executing {self.test_type} test: {str(e)}"
                result.log(error_msg)
                print(f"\nERROR: {error_msg}")
                raise
            finally:
                print("=" * 50)

    return CustomTestSuite()

# Example of adding a new test type
# @register_test("new_test")
class NewExecutionStrategy(TestExecutionStrategy):
    def execute(self, test, app_name: str, stages: List[Stage]) -> Dict[str, Any]:
        return test.run(
            app_name,
            stages,
            # Add any specific parameters needed
        )

# Register the new execution strategy
TestExecutionFactory.register_strategy("new_test", NewExecutionStrategy())


# Note: to add a new test type, you would now just need to:
"""
# 1. Create new execution strategy
@register_test("custom_test")
class CustomExecutionStrategy(TestExecutionStrategy):
    def execute(self, test, app_name: str, stages: List[Stage]) -> Dict[str, Any]:
        return test.run(
            app_name,
            stages,
            # custom parameters
        )

# 2. Register the execution strategy
TestExecutionFactory.register_strategy("custom_test", CustomExecutionStrategy())
"""