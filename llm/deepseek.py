from openai import OpenAI
import os

api_key = os.getenv("API_KEY")

def deepseek_list_model():
    client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
    print(client.models.list())

def deepseek(prompt):
    client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )
    
    response = client.chat.completions.create(
        model="deepseek-chat", # deepseek-coder 
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
      ],
        max_tokens=4096,
        temperature=0.3,
        stream=False,
        frequency_penalty=0,
        presence_penalty=0,
        top_p=1,
        logprobs=False,
        # top_logprobs=3
    )
    print(response.choices[0].message.content)

#deepseek_list_model()
deepseek("who r u")
