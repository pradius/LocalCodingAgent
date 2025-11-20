import logging
from .planner import Planner
from .executor import Executor
from .memory import Memory

class Agent:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.memory = Memory()
        self.planner = Planner(config["planner"])
        self.executor = Executor(config["executor"])

    def run(self, task):
        self.logger.info(f"Starting task: {task}")
        plan = self.planner.create_plan(task)
        self.logger.info(f"Created plan: {plan}")
        result = self.executor.execute_plan(plan, self.memory)
        self.logger.info(f"Finished task with result: {result}")
        return result
