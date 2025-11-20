"""
Unit tests for the Agent class.
"""

import unittest
from unittest.mock import MagicMock
from src.agent.agent import Agent

class TestAgent(unittest.TestCase):
    """
    Test suite for the Agent class.
    """

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.agent = Agent()
        # Mock the components to isolate the agent's logic
        self.agent.example_component = MagicMock()

    def test_agent_initialization(self):
        """
        Test that the agent is initialized correctly.
        """
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.example_component)

    def test_run_calls_component(self):
        """
        Test that the agent's run method calls its components.
        """
        self.agent.run()
        self.agent.example_component.do_something.assert_called_once()

    def test_plan_task(self):
        """
        Test the task planning functionality.
        """
        task_description = "Create a new feature."
        plan = self.agent.plan_task(task_description)
        self.assertIsInstance(plan, list)
        self.assertTrue(len(plan) > 0)

    def test_execute_plan(self):
        """
        Test the plan execution functionality.
        """
        # This is a simple test. A more complex scenario would involve
        # mocking the outcomes of each step.
        plan = ["Step 1", "Step 2"]
        try:
            self.agent.execute_plan(plan)
        except Exception as e:
            self.fail(f"execute_plan raised an exception unexpectedly: {e}")

if __name__ == '__main__':
    unittest.main()
