from zhipuai import ZhipuAI
import os

api_key = os.getenv('API_KEY')

def zhipu_glm(prompt):
    client = ZhipuAI(api_key=api_key) # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
            {"role": "user", "content": f"{prompt}"},
        ],
        stream=False,
    )
    print(response.choices[0].message)
