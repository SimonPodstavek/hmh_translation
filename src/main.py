import os
from os.path import join, abspath

import tiktoken
import requests
import openai.embeddings_utils
import openai
import pandas as pd
import numpy as np
import re

cwd = os.getcwd()
paragraph_embeddings_df = pd.read_csv((join(cwd, 'src\source\paragraph_embeddings.csv')), encoding='ansi')

# def get_embedding(text, model="text-embedding-ada-002"):
#    text = text.replace("\n", " ")
#    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']



def get_translated_paragraph() -> str:
    print("Zadaje obsah prekladu. Pre uloženie stlačte Ctrl-Z.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    contents = ''.join(contents)
    contents = contents.replace('\xa0', '')






headers = {
    'Content-Type': 'application/json',
    'Authorization': ''.join(['Bearer ', os.environ['OPENAI_API_KEY']])
}



# json = {
#     'model': 'text-embedding-ada-002',
#     'input': """
#         Service activities of MIREL VZ1 train protection system represent a set of activities aiming HW and/or SW upgrade and/or change of system configuration in extent of existing documented HW and SW changes and modifications.
#         A part of system upgrade services are service activities focused on change of system function properties in extent of available system function properties .
#         Upgrade service activities neither comprise development activities focused on extension or changes of available function properties, available HW modifications, nor other development activities on MIREL products.
#     """
# }


json = {
    'model':'gpt-3.5-turbo',
    'max_tokens':1000,
    'temperature': 2,
    'messages' : [
        {"role": "system", "content":"""
            You will be provided with a sentences in Hungarian, and your task is to translate them to English. The following paragraphs are related to certification of train control systems. Translate it, so that it sounds professional.The text should be of the same length. You are allowed to change structure of a sentence a little.
            """},
        {"role": "user", "content":"""
            A HMH s.r.o. fenti tárgyban előterjesztett kérelmének, annak érdemi vizsgálatát követően
helyt adok,
és a MIREL VZ1 berendezés v04 (kompiláció 13) szoftver és MIREL STB berendezés v03 (kompiláció 13) szoftver alkalmazását feltételekkel

        """}]
}



# response = requests.post('https://api.openai.com/v1/embeddings',json=json, headers=headers)


response = requests.post('https://api.openai.com/v1/chat/completions',json=json, headers=headers)

print(response.text)


# def num_tokens_from_string(string: str, encoding_name: str) -> int:
#     """Returns the number of tokens in a text string."""
#     encoding = tiktoken.get_encoding(encoding_name)
#     num_tokens = len(encoding.encode(string))
#     return num_tokens

# input_string = """

# """





# print(num_tokens_from_string(input_string, "cl100k_base"))


def mediator() -> None:





if __name__ == '__main__':
    mediator()    