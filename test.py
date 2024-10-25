import json
from pathlib import Path
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

current_dir = Path(__file__).resolve().parent
topic_file = current_dir.parent.parent.parent / 'data' / 'itemCorpus.json'
refer_file = current_dir.parent.parent.parent / 'data' / 'conceptRefs.json'

class Template:
    """
    A class to define a chat template for a chatbot specializing in Media Education and Media Pedagogy.
    """
    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", """
    You are a helpful and knowledgeable chatbot specializing in Media Education and Media Pedagogy. Your task is to assist students with their term papers in the final semester of the Bachelor of Arts program in Culture and Social Sciences at FernUniversität Hagen.

    The students submit their draft of a team paper to you for feedback and recommendations. 

    Your response should include the following:
    Suggest at least two relevant references. Here is the list of suggested references : 
    {context}
    - Provide the response in {language} language. Please note that reference books names and authors should be as it is (i.e in English)
    - Response should be in 150-200 words.
    - Response should begin with text - For Ex. For English :'After understanding your topics, we here initially recommend you two references for your further reading as followings,...'
    
             """),
            ("human", "{user_input}"),
        ]
    )

class TopicsList(BaseModel):
    """
    A Pydantic model to define the structure of topics list.
    """
    topic: str = Field(description="Extracted from user text")
    subject_explaination: str = Field(description="Short text about each subject")
    related_categories: list = Field(description="A list of categories that must be found in the allowed categories below")

class ContextGeneration:
    """
    A class to generate context for term papers using a language model.
    """
    def __init__(self, term_paper_string, llm_model):
        """
        Initialize the ContextGeneration class.

        Parameters:
        term_paper_string (str): The term paper content provided by the user.
        llm_model: The language model to be used for processing.
        """
        self.term_paper_string = term_paper_string
        self.model = llm_model
        self.chain_of_thought = f"""Chain-of-Thought : 
        
        Step 1 : Understanding the input from student which includes term paper, research topic and research questions :
        {self.term_paper_string}
        Recommendation Engine selected : Knowledge Based
        Large Language Model selected : {self.model}
        """
        
    def generate_chain_of_thought(self):
        """
        A helper method to build the chain of thought step-by-step.
        """
        self.chain_of_thought += self._append_relevant_topics()
        self.chain_of_thought += self._append_relevant_references()

    def _append_relevant_topics(self):
        """
        Append relevant topics to the chain of thought.

        Returns:
        str: A string representation of the relevant topics.
        """
        try:
            self.relevant_topics = self.find_relevant_topics()
            return f"""\n\nStep 2: Relevant Topics:\n{self.relevant_topics}"""
        except Exception:
            self.relevant_topics = []
            return "\n\nStep 2: Relevant Topics:\nNo relevant topics found."

    def _append_relevant_references(self):
        """
        Append relevant references to the chain of thought.

        Returns:
        str: A string representation of the relevant references.
        """
        try:
            self.relevant_references = self.find_relevent_refs(self.relevant_topics)
            return f"""\n\nStep 3: Relevant References:\n{self.relevant_references}"""
        except Exception:
            self.relevant_references = "No relevant references found"
            return "\n\nStep 3: Relevant References:\nNo relevant references found."

    def main(self):
        """
        Main method to generate the chain of thought and format relevant references.

        Returns:
        tuple: A tuple containing formatted references and the chain of thought.
        """
        try:
            self.generate_chain_of_thought()
            return self.format_relevant_refs(self.relevant_references), self.chain_of_thought
        except Exception as e:
            return "No references found", self.chain_of_thought

    def openfile(self, filename):
        """
        Open and read a JSON file.

        Parameters:
        filename (str): The path to the JSON file.

        Returns:
        list: A list of data from the JSON file.
        """
        try:
            with open(filename, 'r') as file:
                result_list = json.load(file)
            return result_list
        except Exception as e:
            return []

    def get_topic_list(self):
        """
        Retrieve a flat list of topics from the topic file.

        Returns:
        list: A list of topics.
        """
        topics = self.openfile(topic_file)
        topic_list = []
        for topic in topics:
            topic_list.extend(topic['category'])
        return topic_list
    
    def validate_structure(self, data):
        """
        Validate the structure of the data.

        Parameters:
        data (list): The data to be validated.

        Returns:
        bool: True if the structure is valid, False otherwise.
        """
        if not isinstance(data, list):
            return False
        
        for item in data:
            if not isinstance(item, dict):
                return False
            
            if 'topic' not in item or not isinstance(item['topic'], str):
                return False
            
            if 'subject_explaination' not in item or not isinstance(item['subject_explaination'], str):
                return False
            
            if 'related_categories' not in item or not isinstance(item['related_categories'], list):
                return False
            
            if isinstance(item['related_categories'], list):
                if not all(isinstance(category, str) for category in item['related_categories']):
                    return False
        return True

    def find_topics(self, categories, max_retries=3):
        """
        Find topics from the user input and related categories.

        Parameters:
        categories (list): A list of allowed categories.
        max_retries (int): Maximum number of retries for finding topics.

        Returns:
        list: A list of topics with related categories.
        """
        parser = JsonOutputParser(pydantic_object=TopicsList)
        prompt = PromptTemplate(
            template="""
            Step 1: Summarize and extract three topics or subjects from the text which the user has provided and give a brief explaination about each.
            Here is the text provided by the user: {user_input}
            
            Step 2: Find a list of related categories for each topic or subject from the allowed categories.The allowed topics are provided in JSON format. 
            
            Remember that : Topics must be found or extracted from the user text. If a topic or subject is mentioned, it must be associated with the correct category in the allowed topics list below. If no topic or related category are found, output an empty list.
            
            Allowed categories: {categories}
            
            The output should be a JSON object of three arrays, where each object has the following format in English:
            \n{format_instructions}\n
            """,
            input_variables=["user_input", "categories"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        
        attempts = 0
        
        while attempts < max_retries:
            try:
                chain = prompt | self.model | parser
                response = chain.invoke(
                    {"user_input": self.term_paper_string, "categories": categories}
                )
                
                if self.validate_structure(response):
                    return response
            except Exception as e:
                attempts += 1

        return [{
            "topic": "",
            "subject_explaination": "",
            "related_categories": []
        }]
    
    def find_references(self, concepts):
        """
        Find references based on related concepts.

        Parameters:
        concepts (list): A list of related concepts.

        Returns:
        tuple: A tuple containing a sorted list of references and the number of references found.
        """
        concept_refers = self.openfile(refer_file)
        reference_list = []
        for cf in concept_refers:
            cf_list = cf['concepts'].split(",")
            intersection_list = [val for val in concepts if val in cf_list]
            count = len(intersection_list)
            if count > 0:
                for item in cf['references']:
                    item['star'] = count
                    if item['Title'] not in [re['Title'] for re in reference_list]:
                        reference_list.append(item)
        sorted_list = sorted(reference_list, key=lambda x: x["star"], reverse=True)
        return sorted_list, len(reference_list)
    
    def find_relevant_topics(self):
        """
        Find relevant topics from the topic list.

        Returns:
        list: A list of relevant topics.
        """
        topics = self.get_topic_list()
        relevant_topics_list = self.find_topics(topics)
        return relevant_topics_list
    
    def find_relevent_refs(self, relevant_topics):
        """
        Find relevant references for each topic.

        Parameters:
        relevant_topics (list): A list of relevant topics.

        Returns:
        list: A list of topics with recommended references.
        """
        N = 2
        for ele in relevant_topics:
            try:
                related_concepts = ele['related_categories']
                result_2, no_found_references = self.find_references(related_concepts)
                refer_N = result_2[:N]
                ele['recommended_references'] = refer_N
            except Exception as e:
                continue
            
        return relevant_topics
    
    def format_relevant_refs(self, relevant_topics):
        """
        Format the relevant references for display.

        Parameters:
        relevant_topics (list): A list of relevant topics with references.

        Returns:
        str: A formatted string of relevant references.
        """
        def format_references(references):
            formatted = ""
            for i, ref in enumerate(references, 1):
                formatted += f"\n{i}. Title: {ref['Title']}\n   Authors: {', '.join(ref['Authors'])}\n   Source: {ref['Source']}\n   Date: {ref['Date']}\n   Summary: {ref['Summary']}\n"
            return formatted
        
        response = ""
        for i, item in enumerate(relevant_topics, start=1):
            topic_letter = chr(64 + i)
            response += f"\n({topic_letter}) Topic: {item['topic']}\n"
            response += f"    Subject Explaination: {item['subject_explaination']}\n"
            response += f"    Related Categories: {', '.join(item['related_categories'])}\n"
            response += f"    Recommended References:\n{format_references(item['recommended_references'])}\n"
        return response