import argparse
from src.agent.agent import Agent
from src.utils.config import load_config
from src.utils.logger import setup_logger

def main():
    parser = argparse.ArgumentParser(description="Local Coding Agent")
    parser.add_argument("--task", type=str, required=True, help="The task for the agent to perform")
    args = parser.parse_args()

    config = load_config("config.yaml")
    setup_logger(config["logging"])

    agent = Agent(config)
    agent.run(args.task)

if __name__ == "__main__":
    main()
