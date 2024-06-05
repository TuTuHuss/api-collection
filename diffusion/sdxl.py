import requests
import os

api_key = os.getenv('API_KEY')

def sdxl_request(prompt,outputimg):
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={
            "none": ''
        },
        data={
            "prompt": prompt,
            "output_format": "png",
            "aspect_ratio": "1:1",
            "seed":42,
            "negative_prompt": ''
    
        },
    )
    
    if response.status_code == 200:
        with open(outputimg, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

sdxl_request('a cat', './cat.png')
