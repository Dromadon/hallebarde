from setuptools import setup, find_packages

setup(
    name="hallebarde",
    version="1.0.0",
    install_requires=["boto3", "botocore", "pyjwt"],
    packages=find_packages(exclude=("tests*",)),
    extras_require={
        "tests": ["behave", "coverage", "docker", "flake8", "mypy", "pytest", "pytest-env", "requests",
                  "requests_oauthlib"]
    }
)
