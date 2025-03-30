from openai import OpenAI


class recraft():
    def __init__(self) -> None:
        self.client = OpenAI(
            base_url='https://external.api.recraft.ai/v1',
            api_key='',
        )

    def text2image(self,prompt:str) -> str:

        response = self.client.images.generate(
            prompt=prompt,
            model='recraftv2', # recraftv3
            style='icon',  # digital_illustration realistic_image etc.
            n=1, # generate picture number
            size='1024x1024', # 1024x1280 2048x1024 etc.
            response_format='url' # b64_json
        )
        return response.data[0].url

