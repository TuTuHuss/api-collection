from pathlib import Path
from openai import OpenAI #openai>=1.0.0  python >=3.7.1
import os

api_key = os.getenv('API_KEY')

class moonshot():

    def __init__(self): 
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1",
        )

    def moonshot_RAG(self,custom_prompt:str,file_path:str=None):
        if file_path is not None:
            file_object = client.files.create(file=Path(file_path), purpose="file-extract")
            file_content = client.files.content(file_id=file_object.id).text
        
            messages=[
                {
                    "role": "system",
                    "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
                },
                {
                    "role": "system",
                    "content": file_content,
                },
                {
                    "role": "user", 
                    "content": f"{custom_prompt}"
                },
            ]
        else:
            messages=[
                {
                    "role": "system",
                    "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
                },
                {
                    "role": "user",
                    "content": f"{custom_prompt}"
                },
            ]
        completion = self.client.chat.completions.create(
          model="moonshot-v1-128k",  #还有8k 32k版本可用
          messages=messages,
          temperature=0.3,
          max_tokens=1024, #聊天完成时生成的最大 token 数与TPM(token per minute, 每分钟交互的token数)有关 目前最大127999。
          top_p=1.0, #另一种采样温度
          n=1, #为每条输入消息生成多少个结果
          stream=False #流式输出
        
        )
        print(completion.choices[0].message)

client = moonshot()
client.moonshot_RAG(custom_prompt='who r u')
client.moonshot_RAG(custom_prompt='who r u', file_path='content.txt')
    
