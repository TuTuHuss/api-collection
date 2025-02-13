#Note: The openai-python library support for Azure OpenAI is in preview.
      #Note: This code sample requires OpenAI Python library version 1.0.0 or higher.

import os
from openai import AzureOpenAI

azure_endpoint = os.getenv('AZURE_ENDPOINT')
api_key = os.getenv('API_KEY')


def send_request(prompt):
    client = AzureOpenAI(
      azure_endpoint = azure_endpoint, 
      api_key=api_key,  
      api_version="2024-02-15-preview"
    )
    
    message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."},
                    {"role": "user", "content": prompt},]
    
    completion = client.chat.completions.create(
      model="gpt-4", # model = "deployment_name"
      messages = message_text,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      #response_format={"type": "json_object"}, support with gpt-35-turbo-1106
      stop=None
    )
    print(completion.choices[0].message.content)
