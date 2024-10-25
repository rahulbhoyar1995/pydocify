# pydocify - LLM-Based Documentation Generator Library for Python Code

#### Author : Rahul Bhoyar

`pydocify` is a library that uses a language model (LLM) to generate and add documentation strings (docstrings) for Python scripts, functions, and classes. This is especially useful for maintaining code readability and consistency in projects with minimal documentation.

### Features
- Automatically generates docstrings based on code content.
- Archives original Python files before documentation is added.
- Recursively processes all Python files in a specified directory.
- Supports deleting archive files created during the documentation process.

### Installation
Install `pydocify` with pip:

```bash
pip install pydocify
```

### Usage

#### 1. Documenting All Python Files in a Directory
Use the DirectoryStringGenerator class to recursively document all Python files in a specified directory:

```bash
from pydocify.core import DirectoryStringGenerator

doc_generator = DirectoryStringGenerator()
doc_generator.generate("/path/to/your/directory")
```
#### 2. Deleting Archive Files during documentation process
Use delete_archives to remove any archive files created during the documentation process:

```bash
doc_generator.delete_archives("/path/to/your/directory")
```

#### 3. Adding Documentation to Python Files
To automatically generate documentation for a specific Python file:

```bash
from pydocify.core import add_doc_to_python_file
from pathlib import Path

add_doc_to_python_file(Path("your_script.py"))
```

### Requirements
Ensure that you have your OPENAI_API_KEY set up as an environment variable in a .env file.

### License
pydocify is licensed under the MIT License.