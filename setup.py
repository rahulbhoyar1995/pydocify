from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

# Read the contents of README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydocify",
    version="0.2",
    description="pydocify: An LLM-based library that effortlessly auto-generates docstrings for your Python scripts and modules, enhancing code readability with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rahul Bhoyar",
    author_email="rahulbhoyaroffice@gmail.com",
    url="https://github.com/rahulbhoyar1995/pydocify.git",
    packages=find_packages(include=["pydocify", "pydocify.*"]),  # Include your package
    install_requires=required_packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,  # Ensures additional files like requirements.txt are included
)
