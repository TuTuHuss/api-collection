import requests
from openai import OpenAI
from typing import Tuple,Dict,List
import base64


class siliconflow():
    # https://docs.siliconflow.cn/api-reference/audio/create-speech
    def __init__(self) -> None:
        self.key =  # str, eg:sk-xxxxxx

        self.headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }

    def upload_reference_audio(self,reference_audio:Tuple[str,str]) -> Dict[str,str]:
        url = "https://api.siliconflow.cn/v1/uploads/audio/voice"
        headers = {"Authorization": f"Bearer {self.key}"}
        audio_file = {"file":open(reference_audio[0],"rb")}
        data = {
            "model": "FunAudioLLM/CosyVoice2-0.5B",
            "customName": , #str, define the reference audio name 
            "text": reference_audio[1]
        }
        response = requests.post(url, headers=headers, files=audio_file, data=data)
        return response.json() # {'uri': '{customName}:14325346'}
    
    def list_reference(self) -> Dict[str,List[Dict[str,str]]]:
        url = "https://api.siliconflow.cn/v1/audio/voice/list"
        headers = {"Authorization": f"Bearer {self.key}"}
        response = requests.request("GET",url,headers=headers)
        return response.json()


    def text2audio(self,text:str,result_file:str="./result.mp3") :
        url = "https://api.siliconflow.cn/v1/audio/speech"
        payload= {
            "model": "FunAudioLLM/CosyVoice2-0.5B",
            "input": text,
            "voice": , # str, eg:FunAudioLLM/CosyVoice2-0.5B:benjamin
            "response_format": "mp3",
            "sample_rate":32000,
            "stream":False,
            "speed":1,
            "gain":0
        }
        
        response = requests.request("POST",url,json=payload,headers=self.headers)

        if response.status_code == 200:
            with open(result_file,'wb')as file:
                file.write(response.content)
            print(f"file saved at {result_file}")
        else:
            print(f"error: status code {response.status_code}")

        

if __name__ == "__main__":
    client = siliconflow()
    #client.upload_reference_audio(reference_audio=("./2435767.wav","1950年第二次世界大战的硝烟已经散去了5年，殖民主义却并没有消亡殆尽，他们仍试图挥舞着自己的爪牙"))
    #client.list_reference()
    #client.text2audio("2024年已经过去，让我们迎接即将到来的新一年")
