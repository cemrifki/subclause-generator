from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="subclause_generator",
    version="0.1.0",
    description="A tool to generate subclauses using dependency parsing methods / rules.",
    author="Cem Rıfkı Aydın",
    packages=find_packages(),  
    install_requires=requirements,
    python_requires=">=3.7",
    include_package_data=True,
)

