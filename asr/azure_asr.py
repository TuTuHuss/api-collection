from openai import AzureOpenAI
import os
from pydub import AudioSegment

azure_endpoint = os.getenv("AZURE_ENDPOINT")
api_key = os.getenv("API_KEY")
azure_deployment = os.getenv("AZURE_DEPLOYMENT")

class OpenAIClient:
    def __init__(self, verbose=False):
        self.client = AzureOpenAI(
            azure_endpoint = azure_endpoint, 
            api_key=api_key,  
            api_version="2024-02-15-preview",
            azure_deployment=azure_deployment,
        )
        self.verbose = verbose

    def transcribe_audio_file(self, file_path):
        audio = AudioSegment.from_file(file_path)
        # Define the chunk size (10 minutes in milliseconds)
        chunk_size = 10 * 60 * 1000
        # Calculate the number of chunks
        num_chunks = len(audio) // chunk_size + (1 if len(audio) % chunk_size else 0)
        transcript = ""

        # Check the size of the file
        file_size = os.path.getsize(file_path)

        # If the file size is less than 24 MB, transcribe it directly
        if file_size <= 24 * 1024 * 1024:
            with open(file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper",
                    file=audio_file,
                    response_format="text"
                )
        else:
            # If the file size is more than 24 MB, chunk it
            for i in range(num_chunks):
                # Extract the chunk
                chunk = audio[i*chunk_size:(i+1)*chunk_size]
                # Save the chunk to a temporary file
                temp_chunk_path = os.path.join(os.path.dirname(file_path), "temp_chunk.mp3")
                chunk.export(temp_chunk_path, format="mp3")
                # Transcribe the chunk
                with open(temp_chunk_path, "rb") as audio_file:
                    chunk_transcript = self.client.Audio.transcribe("whisper", audio_file)
                # Append the chunk transcript to the overall transcript
                transcript += chunk_transcript
                # Delete the temporary chunk file
                os.remove(temp_chunk_path)

        if self.verbose:
            print(f"Transcription successful for file: {file_path}")

        return transcript

client = OpenAIClient(verbose=True)
print(client.transcribe_audio_file("hello_world.mp3"))
