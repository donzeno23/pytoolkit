# test_plan_performance.py

from testplan import Testplan
from testplan.testing.multitest import MultiTest

from stages import get_replay_stages, get_performance_stages, get_recovery_stages
from test_suites import create_test_suite

class AppTestFacade:
    def __init__(self):
        self.apps = {}
        self.testplan = Testplan(name="AppTests")

    def register_app(self, app_name: str, test_stages: dict):
        self.apps[app_name] = test_stages

    def create_multitest(self, app_name: str):
        test_suites = []
        
        for test_type, stages in self.apps[app_name].items():
            test_suite = create_test_suite(test_type, stages, app_name)
            print(f"Created test suite for {app_name} - {test_type}")
            print(f"adding test suite: {test_suite.name} to multitest.")
            test_suites.append(test_suite)

        multitest = MultiTest(
            name=app_name,
            suites=test_suites
        )
        self.testplan.add(multitest)

    def run_all_tests(self):
        for app_name in self.apps:
            self.create_multitest(app_name)
        self.testplan.run()

if __name__ == "__main__":
    facade = AppTestFacade()

    # Register app with stages
    facade.register_app("MyApp", {
        "replay": get_replay_stages(),
        "performance": get_performance_stages(),
        "recovery": get_recovery_stages(),
    })

    # Run tests using Testplan
    facade.run_all_tests()
