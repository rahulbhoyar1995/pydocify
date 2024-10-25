"""
pydocify.core - A module for generating and adding docstrings to Python files using a language model (LLM).

This module provides functionality to automatically document Python files by generating docstrings
with a language model, as well as functionality for handling documentation files and managing archives.

Classes:
    DirectoryStringGenerator: Handles generating docstrings for all Python files in a specified directory and managing archive files.

Functions:
    add_doc_to_python_file(file_path: Path): Adds generated documentation to a specified Python file.
"""

import os
import re
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from tqdm import tqdm

# Load environment variables from a .env file
_ = load_dotenv(find_dotenv())

def add_doc_to_python_file(file_path: Path):
    """
    Adds documentation to a specified Python file by invoking a language model.

    This function reads the content of a Python file, generates documentation
    using a language model, and writes the updated content back to the file.
    It also archives the original file.

    Parameters:
    file_path (Path): The path to the Python file to be documented.

    Returns:
    None

    Raises:
    KeyError: If the OPENAI_API_KEY environment variable is not set.
    FileNotFoundError: If the specified file does not exist.
    IOError: If there is an error reading or writing the file.
    Exception: If there is an error invoking the language model.
    """
    try:
        openai_api_key = os.environ["OPENAI_API_KEY"]
    except KeyError:
        print("Error: The OPENAI_API_KEY environment variable is not set.")
        return

    try:
        # Read the existing code from the file
        python_file_content = file_path.read_text()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return
    except IOError as e:
        print(f"Error reading the file '{file_path}': {e}")
        return

    # Create a prompt to generate the updated code with documentation
    tagging_prompt = ChatPromptTemplate.from_template(
        """
        As a highly skilled documentation specialist with expertise in Python scripting, your assignment is to meticulously review a specified Python file. Focus on analyzing the functions, classes, and module structure to add clear, concise, and essential documentation in accordance with PEP 8 standards. Each docstring should thoroughly describe the purpose of each element, covering parameters, return values, and any exceptions that may be raised. Remove unnecessary modules if they are not used in the script. Arrange the imports as per PEP-8 guidelines.

        Identify potential points of failure and incorporate try-except blocks to handle exceptions gracefully, particularly where input validation or complex processing could result in runtime errors. Validate function and class inputs and outputs where appropriate to ensure code robustness and error prevention.

        Provide the revised code in a plain-text format, without any additional symbols, formatting, or delimiters. 
        Note that you must not include any expressions surrounded by backticks in the text as they are no longer supported by Python. Do not include backticks at the beginning or end of the code.
        Here is the code:
        {code}
        """
    )

    try:
        # Invoke the language model with the prompt
        llm = ChatOpenAI(temperature=0, model="gpt-4o")
        tagging_chain = tagging_prompt | llm
        response = tagging_chain.invoke({"code": python_file_content})
    except Exception as e:
        print(f"Error invoking the language model: {e}")
        return

    # Get the updated content
    updated_content = response.content

    # Remove backticks if they still appear in the output
    updated_content = re.sub(r'^```.*|```$', '', updated_content, flags=re.MULTILINE).strip()

    # Rename the original file to "file_name_archive.py"
    archive_file_path = file_path.with_name(f"{file_path.stem}_doc_archive.py")
    try:
        file_path.rename(archive_file_path)
    except IOError as e:
        print(f"Error renaming the file '{file_path}': {e}")
        return

    # Write the updated content to a new file with the original file name
    try:
        file_path.write_text(updated_content)
    except IOError as e:
        print(f"Error writing to the file '{file_path}': {e}")
        return

    print(f"Original file renamed to '{archive_file_path}'.")
    print(f"Documentation added and file '{file_path}' has been updated with the new content.")

class DirectoryStringGenerator:
    def __init__(self):
        pass
    
    def generate(directory_path: str):
        """
        Finds and documents all Python files in a specified directory and its subdirectories.

        Parameters:
        directory (Path): The path to the directory to search for Python files.

        Returns:
        None
        """
        directory = Path(directory_path)
        python_files = []

        # Walk through the directory to find all .py files
        for file_path in directory.rglob('*.py'):
            python_files.append(file_path)

        total_files = len(python_files)
        print(f"Total Python files found: {total_files}")

        # Process each Python file with progress tracking
        for file_path in tqdm(python_files, desc="Adding documentation to Python files..."):
            add_doc_to_python_file(file_path)
            
    def delete_archives(self,directory_path: str):
        """
        Deletes all files in the specified directory and its subdirectories
        that end with '_doc_archive.py'.

        Parameters:
        directory (Path): The path to the directory to search for archive files.

        Returns:
        None
        """
        directory = Path(directory_path)
        # Find all files that end with '_doc_archive.py'
        archive_files = list(directory.rglob('*_doc_archive.py'))

        total_files = len(archive_files)
        print(f"Total archive files found: {total_files}")

        # Delete each file and show progress
        for file_path in tqdm(archive_files, desc="Deleting archives files...."):
            try:
                file_path.unlink()  # Delete the file
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

