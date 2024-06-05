import requests
import time
import jwt  #PyJWT==2.6.0, please don't run 'pip install jwt', if you already installed jwt, please uninstall both two of them and rerun 'pip install PyJWT==2.6.0'
import json
import sys
import os

ak = os.getenv('MH_AK')
sk = os.getenv('MH_SK')

class mh_newapi_t2i():

    def __init__(self) -> None:
        self.ak = f"{ak}"
        self.sk = f"{sk}"
        self.prompt_parameter ={
            # custom settings
            "prompt" : 'league of legends', #必需, string, 正向描述词
            "neg_prompt" : "low quality, pink", #非必需, string, 反向描述词 
            "samples" : 2, #非必需, int, 范围[1,8]， default=1， 生成图片的数量
            "height" : 960, #非必需, int, 范围[640, 6144], default=960, 图片高度 
            "width" : 960, #非必需, int, 范围[640, 6144], default=960, 图片宽度
            "cfg_scale" : 7.0, #非必需, float, 范围[1,20], default=7.0, 提示文本的控制力度（数字越大，生成的图片跟提示词相关性越强）
            # generage settings
            "model_id" : "sgl_artist_v0.3.5_0925", #必需, string, 其他可用模型请参考get_model_id()方法
            "vae" : "vae_sd_84000", #非必需, string, default="vae_sd_84000", 画面色彩调节   others: vae_sd_84000, vae_sd1.5, vae_anime, default
            "seed" : 42, #非必需, int, 范围[0,9999999), default=0, 随机数种子
            "step": 50, #非必需, int, 范围[30,150], default=50, 运行的扩散步骤数
            "sampler" : 'DDIM' #非必需, string, default="DDIM", 扩散过程中的采样器
        }

    def get_token(self):
        headers = {
            "alg":"HS256",
            "typ":"JWT",
        }
        parameter = {
            "iss": self.ak,
            "exp": int(time.time()) + 3600,
            "nbf": int(time.time()) -5,
        }
        token = jwt.encode(parameter, self.sk, headers=headers)
        return token
    
    def get_model_id(self):
        url = 'https://api.sensenova.cn/v1/imgen/models'
        headers = {
            "Authorization": self.get_token(),
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        print(response.text)

    def submit_task(self):
        url = 'https://api.sensenova.cn/v1/imgen/internal/generation_tasks'
        headers = {
            "Authorization": self.get_token(),
            "Content-Type": "application/json",
        }
        print(f'Submitting task for *** {self.prompt_parameter["prompt"]} ***')
        while True:
            try:
                response = requests.post(url, json=self.prompt_parameter, headers=headers)
                break
            except Exception as e:
                print(e)
                time.sleep(5)
                continue
        task_id = json.loads(response.text).get('task_id')
        print(f"Task submitted, task_id: {task_id}")
        return task_id
    
    def get_result(self):
        task_id = self.submit_task()
        url = f"https://api.sensenova.cn/v1/imgen/internal/generation_tasks/{task_id}" # single task url
        headers = {
            "Authorization": self.get_token(),
            "Content-Type": "application/json",
        }
        # url = "https://api.sensenova.cn/v1/imgen/internal/generation_tasks" # task list url
        # parameter = {
        #     "task_id": task_id,
        # }
        # result = requests.get(url,params=parameter, headers=headers) # task list requests
        while True:
            try:
                response = requests.get(url, headers=headers).json()
                if response["task"]["state"] == "PENDING":
                    print("Task queued")
                    time.sleep(3)
                    continue
                elif response["task"]["state"] == "RUNNING":
                    print("image generating...")
                    time.sleep(5)
                    continue
                elif response["task"]["state"] == "SUCCESS":
                    print("image generated")
                    break
                elif response["task"]["state"] == "FAILED":
                    print(f"Task failed, task id : {task_id}")
                    sys.exit(1)
            except Exception as e:
                print(e)
                sys.exit(1)
        for i in range(0,self.prompt_parameter["samples"]):
            download_url = response["task"]["result"][i]["raw"]
            current_dir = os.getcwd()
            file_path = os.path.join(current_dir, f'{task_id}-{i}.jpg')
            with open(file_path, 'wb') as f: 
                f.write(requests.get(download_url).content) 
                print(f"Image {task_id}-{i} saved at: {file_path}")

if __name__ == "__main__":
    task = mh_newapi_t2i()
    task.get_result()




