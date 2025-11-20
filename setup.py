from setuptools import setup, find_packages

setup(
    name="local-coding-agent",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"":"","src"},
    install_requires=[
        "fastapi",
        "langchain",
        "langchain-community",
        "langchain-core",
        "langchain-openai",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "black",
        ],
    },
    entry_points={
        "console_scripts": [
            "local-coding-agent=main:main",
        ],
    },
)
