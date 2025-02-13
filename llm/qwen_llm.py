from openai import OpenAI
import os

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

def get_response(prompt):
    client = OpenAI(
        api_key = api_key,
        base_url = base_url,  # 填写DashScope SDK的base_url
    )
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': f'{prompt}'}],
        stream=False,
        top_p=0.9,
        temperature=0.3,
        max_tokens=1024,
        seed=42,
        )
    for chunk in completion:
        print(chunk.choices[0].message)

    get_response('who r u')
