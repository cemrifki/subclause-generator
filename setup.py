from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="subclause_generator",
    version="0.2.0",
    description="A tool to generate subclauses using dependency parsing methods / rules for both English and Turkish.",
    author="Cem Rifki Aydin",
    packages= ["subclause_generator"],  # find_packages(),  
    install_requires=requirements,
    python_requires=">=3.9",
    include_package_data=True,
)

