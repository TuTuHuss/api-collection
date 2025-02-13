from httpx import stream
from zhipuai import ZhipuAI
import base64

class glm4vFlash():
    #https://bigmodel.cn/dev/api/normal-model/glm-4v
    def __init__(self) -> None:
        self.client = ZhipuAI(api_key='')


    def image_local(self,img_path:str) -> str:

        with open(img_path,'rb') as img:
            img_base = base64.b64encode(img.read()).decode('utf-8')

        response = self.client.chat.completions.create(
            model='glm-4v-flash',
            do_sample=True,
            stream=False,
            temperature=0.7,
            top_p=0.95,
            max_tokens=1024,
            messages=[
            {
                "role": "user",
                "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": img_base
                    }
                },
                {
                    "type": "text",
                    "text": "请描述这个图片"
                }
                ]
            }
            ]
        )
        return response.choices[0].message.content


    def image_web(self,img_url:str) -> str:
        response = self.client.chat.completions.create(
            model="glm-4v-flash",  # 填写需要调用的模型名称
            do_sample=True,
            stream=False,
            temperature=0.7,
            top_p=0.95,
            max_tokens=1024,
            messages=[
               {
                "role": "user",
                "content": [
                  {
                    "type": "text",
                    "text": "图里有什么"
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                        "url" : img_url
                    }
                  }
                ]
              }
            ]
        )
        return response.choices[0].message.content

