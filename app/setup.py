from setuptools import setup, find_packages

setup(name="hallebarde",
      version="1.0.0",
      install_requires=["boto3"],
      packages=find_packages(exclude=("tests*",)),
      extras_require={"tests": ["pytest", "pytest-mock"]})
