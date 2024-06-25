from dotenv import load_dotenv
import os
load_dotenv()
# from read_files import read_text_file
# from langchainutils import create_simple_chain
# from search import searchChunk, searchDocs
# from utils_from_aless import *
import tiktoken
from typing import AsyncIterable
from typing import List, Dict, Tuple, Optional, TypedDict
import re
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.docstore.document import Document
from langchain.output_parsers import (
    OutputFixingParser,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.output_parsers import PydanticOutputParser
from azure.core import MatchConditions
import uuid
import random
from typing import Tuple, List, Dict
import json
from typing import Type, Optional, Dict
# from langchain_core.tools import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
# from search import searchChunk, searchDocs
from langchain.tools import BaseTool, StructuredTool, tool
import json
from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.prompts import format_document
from langchain.memory.entity import BaseEntityStore
from datetime import datetime, UTC
from langchain_core.runnables import RunnablePassthrough, Runnable
from typing import List, Dict, Tuple, Optional, AsyncIterable, Any, Mapping
from langchain_core.runnables.base import RunnableSerializable

from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from typing import List, Type, Dict, TypeVar, Any, Union, Optional, NotRequired
from pathlib import Path
from functools import cache
import re

from enum import StrEnum
from langchain.prompts import PromptTemplate

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, OpenAI, ChatOpenAI
llm = ChatOpenAI(
    model_name="gpt-4o", openai_api_key=os.environ["OPENAI_API_KEY"], openai_organization=os.environ["OPENAI_ORGANIZATION"],
    temperature=0.3,
    streaming=True,
    request_timeout=60)

import os
import ast

def list_python_files(path):
    """
    List all Python files in the given directory path.
    """
    python_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def get_functions_definitions(file_path):
    with open(file_path, 'r', encoding = 'utf-8') as file:
        source_code = file.read()
        tree = ast.parse(source_code)
        function_definitions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_code = ast.get_source_segment(source_code, node)
                function_definitions.append(function_code)

        return source_code
    
    

function_prompt = """Can you write me a detailed docstrings for each function and classes you find in the python file in this path: {name}.
Here is the code: {contenu}.
Please just provide the function name or class name and the docstrings as such: {{'function_name': 'function.py', 'docstring': '..Initializes the main application window and its components..'}}, nothing else. 
The format to follow: {format_instructions}"""
# class_prompt = """Can you write me a detailed docstring for each classes you find here: {}. 
# Each of the functions of these classes are described by the docstrings: {}"""

def generate_function_doc(names: list[str], prompt:str) -> str:
    if not names:
        raise("You forgor bro")
    fonc_defs = []
    
    prompt1 = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert in python coding."),
            ("human", prompt)
        ]
    )
    # Simple chain
    class docy(BaseModel):
        class_or_function: str = Field(description="This field can only be 'class' if it is a class or 'function' if it is a function.")
        class_of_the_function: str = Field(description="When it is a function, we need to know from which class it belongs to. Use the class name of the function.")
        function_name: str = Field(description="Name of the function or class found in the file.")
        docstring: str = Field(description="The very detailed docstring of the function or the class.")
    parser = JsonOutputParser(pydantic_object=docy)

    for name in names:
        prout = get_functions_definitions(name)
        if prout:
            fonc_defs.append({'name': name, 'contenu': prout, 'ai_generated': '', 'format_instructions': parser.get_format_instructions()})

    chain1 = prompt1 | llm | parser

    explains = []
    for dico in fonc_defs:
        explains.append(chain1.invoke(dico))  
    i = 0
    for elem in fonc_defs:
        elem['docstring'] = explains[i]
        i+=1
    return fonc_defs