import argparse
from .agent.base_agent import BaseAgent

def main():
    """Main entry point for the coding agent."""
    parser = argparse.ArgumentParser(description='Local Coding Agent')
    parser.add_argument('task', type=str, help='The coding task for the agent to perform')
    args = parser.parse_args()

    agent = BaseAgent()
    result = agent.run(args.task)

    print(f'Agent finished task with result: {result}')

if __name__ == '__main__':
    main()
