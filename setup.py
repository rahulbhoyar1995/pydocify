from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setup(
    name="pydocify",
    version="0.1.0",
    description="A LLM based customised library to generate documentation strings for Python scripts.",
    author="Rahul Bhoyar",
    author_email="rahulbhoyaroffice@gmail.com",
    url="https://github.com/rahulbhoyar1995/pydocify.git",
    packages=find_packages(),
    install_requires=required_packages,  # Set requirements from the file
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
