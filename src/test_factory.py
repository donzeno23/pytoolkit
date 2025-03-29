# test_factory.py

from abc import ABC, abstractmethod
from stages import Stage
from typing import Optional

class Test(ABC):
    @abstractmethod
    def run(self, app_name: str, stages: list[Stage], **kwargs):
        pass

class ReplayTest(Test):
    def run(self, app_name: str, stages: list[Stage], log_path: str, batch_data: dict, **kwargs):
        results = {}
        for stage in stages:
            if stage.name == "connect":
                results[stage.name] = stage.execute(app_name)
            elif stage.name == "get_log":
                results[stage.name] = stage.execute(app_name)
            elif stage.name == "read_log":
                results[stage.name] = stage.execute(log_path)
            elif stage.name == "inject_data":
                results[stage.name] = stage.execute(batch_data)
            else:
                results[stage.name] = stage.execute(results)
        return results

class PerformanceTest(Test):
    def run(self, app_name: str, stages: list[Stage], batch_data: dict, **kwargs):
        results = {}
        for stage in stages:
            results[stage.name] = stage.execute(
                app_name if stage.name == "connect"
                else batch_data if stage.name == "send_batch"
                else results
            )
        return results

class RecoveryTest(Test):
    def run(self, app_name: str, stages: list[Stage], **kwargs):
        results = {}
        for stage in stages:
            results[stage.name] = stage.execute(
                app_name if stage.name == "connect"
                else "dummy_recovery_log.txt" if stage.name == "read_log"
                else results
            )
        return results

class TestFactory:
    """Factory class using registry pattern"""
    _registry: dict[str, type[Test]] = {}
    _instance: Optional['TestFactory'] = None

    def __new__(cls):
        """Singleton pattern if needed"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, test_type: str, test_class: type[Test]) -> None:
        """Register a test class with validation"""
        if not issubclass(test_class, Test):
            raise ValueError(f"Class {test_class.__name__} must inherit from Test")
        if test_type in cls._registry:
            raise ValueError(f"Test type '{test_type}' is already registered")
        cls._registry[test_type] = test_class

    @classmethod
    def unregister(cls, test_type: str) -> None:
        """Unregister a test type"""
        cls._registry.pop(test_type, None)

    @classmethod
    def get_registered_types(cls) -> list[str]:
        """Get list of registered test types"""
        return list(cls._registry.keys())

    @classmethod
    def create_test(cls, test_type: str) -> Test:
        """Create a test instance with error handling"""
        try:
            test_class = cls._registry[test_type]
            return test_class()
        except KeyError:
            available_types = ", ".join(cls.get_registered_types())
            raise ValueError(
                f"Unknown test type: {test_type}. "
                f"Available types are: {available_types}"
            )

# Register test types
TestFactory.register("replay", ReplayTest)
TestFactory.register("performance", PerformanceTest)
TestFactory.register("recovery", RecoveryTest)

# Optional: Create a decorator for easier registration
def register_test(test_type: str):
    """Decorator to register test classes"""
    def decorator(cls):
        TestFactory.register(test_type, cls)
        return cls
    return decorator

"""
# Example of using the decorator for a new test type
@register_test("new_test")
class NewTest(Test):
    def run(self, app_name: str, stages: list[Stage], **kwargs):
        # Implementation for new test type
        pass
"""