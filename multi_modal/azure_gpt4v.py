from openai import AzureOpenAI
import base64
from mimetypes import guess_type
import os

api_base = os.getenv("API_BASE")
api_key = os.getenv("API_KEY")
deployment_name = os.getenv("DEPLOYMENT_NAME")

def local_image_to_data_url(img_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(img_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(img_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

def gpt4v(text_prompt :str, img_path :str):
    
    
    client = AzureOpenAI(
        api_key=api_key,  
        api_version='2024-02-15-preview',
        base_url=f"{api_base}/openai/deployments/{deployment_name}"
    )
    
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": text_prompt 
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": local_image_to_data_url(img_path) # also allowed a web image path, like "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg"
                    }
                }
            ] } 
        ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
    )  
    print(response.choices[0].message.content)


gpt4v('describe this picture', '20240408-130122.jpeg')
