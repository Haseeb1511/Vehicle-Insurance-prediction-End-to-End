#  it help in using function that are define inside src folder to use them outside the src folder in root directory or any other
# Use functions, classes, and modules inside the src/ folder from anywhere in your project, including the root directory or other scripts — without messing

from setuptools import setup,find_packages

setup(
    name="src",
    version="0.0.1",
    author="haseeeb",
    author_email="haseebmanzoor1511@gmail.com",
    packages=find_packages())


#setuptools is a Python library used for packaging Python projects.
# setup is a function that defines the package metadata and configuration.
# find_packages() automatically discovers all sub-packages inside your project (i.e., folders with __init__.py files).


# packages=find_packages()
# Automatically includes all sub-packages inside the directory for installation (like src.module1, src.utils, etc.).