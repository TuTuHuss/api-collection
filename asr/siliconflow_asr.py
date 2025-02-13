import requests

def asr_request(file_path:str,file_type:str="audio/wav",model_name:str="FunAudioLLM/SenseVoiceSmall"):
    
    url = "https://api.siliconflow.cn/v1/audio/transcriptions"

    with open(file_path, "rb") as audio_file:
        files = {
            "file": ("audio_file.wav", audio_file, file_type),
            "model": (None, model_name, "text/plain")
        }
    
        headers = {
            "Authorization": "Bearer sk-" # api token
        }
    
        response = requests.post(url, files=files, headers=headers)
    
    print(response.status_code)
    print(response.text)

asr_request("1.wav")
