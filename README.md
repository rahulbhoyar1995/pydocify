# pydocify - LLM-Based Documentation Generator Library for Python Code


![Logo](assets/pydocify_logo.png) <!-- Set the width to 400 pixels -->


#### Author : Rahul Bhoyar

### Transform Your Python Code with pydocify!

Unlock the power of documentation with pydocify, an innovative LLM-based library that automatically generates clear and concise docstrings for your Python scripts and modules. Say goodbye to the hassle of writing documentation from scratch! Whether you're maintaining a small project or collaborating on a large codebase, pydocify enhances code readability and consistency, ensuring your functions and classes are well-documented and easy to understand. Elevate your coding experience and keep your projects organized with just a few simple commands!

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


#### 3. Documenting a Python File 
Use the FileStringGenerator class to document a Python file at specified path:

```bash
from pydocify.core import FileStringGenerator

file_doc_generator = FileStringGenerator()
file_doc_generator.generate("/path/to/your/file")
```

### Requirements
Ensure that you have your OPENAI_API_KEY set up as an environment variable in a .env file.

### License
pydocify is licensed under the MIT License.