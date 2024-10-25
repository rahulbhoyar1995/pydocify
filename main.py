import os
import re
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Load environment variables from a .env file
_ = load_dotenv(find_dotenv())

def add_doc_to_python_file(file_path):
    """
    Adds documentation to a specified Python file by invoking a language model.

    This function reads the content of a Python file, generates documentation
    using a language model, and writes the updated content back to the file.
    It also archives the original file.

    Parameters:
    file_path (str): The path to the Python file to be documented.

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
        with open(file_path, "r") as file:
            python_file_content = file.read()
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
    archive_file_path = f"{file_path.rsplit('.', 1)[0]}_archive.py"
    try:
        os.rename(file_path, archive_file_path)
    except IOError as e:
        print(f"Error renaming the file '{file_path}': {e}")
        return

    # Write the updated content to a new file with the original file name
    try:
        with open(file_path, "w") as file:
            file.write(updated_content)
    except IOError as e:
        print(f"Error writing to the file '{file_path}': {e}")
        return

    print(f"Original file renamed to '{archive_file_path}'.")
    print(f"Documentation added and file '{file_path}' has been updated with the new content.")

add_doc_to_python_file("test.py")