import requests

class siliconflow():
    def __init__(self):
        self.url = "https://api.siliconflow.cn/v1/chat/completions"
        self.headers = {
            "Authorization": "Bearer sk-", # api token
            "Content-Type": "application/json"
        }

    def deepseek(self,prompt:str="中国大模型行业2025年将会迎来哪些机遇和挑战？"):
        payload = {
            "model": "deepseek-ai/DeepSeek-V3", # deepseek-ai/DeepSeek-R1
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "max_tokens": 512,
            "stop": ["null"],
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"},
            # "tools": [
            #     {
            #         "type": "function",
            #         "function": {
            #             "description": "<string>",
            #             "name": "<string>",
            #             "parameters": {},
            #             "strict": False
            #         }
            #     }
            # ]
        }
        response = requests.request("POST", self.url, json=payload, headers=self.headers)
        return response.text

    

a=siliconflow()
print(a.deepseek())
