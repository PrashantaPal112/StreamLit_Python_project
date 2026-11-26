from google import genai
from dotenv import load_dotenv
import os
import io
from gtts import gTTS

load_dotenv()

genai.api_key = os.getenv("GENAI_API_KEY")

#initialize a client
client = genai.Client(api_key=genai.api_key)

#Note Generator Function

def note_generator(images):
    prompt="""
    Summarize the content of the images and use markdown to make interactive notes. 
    If the image has Bangla text language the summarize it in Bangla. 
    If the image has English text language the summarize it in English.
     """
    response=client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[images,prompt]
    )
    return response.text

def audio_transcription(text):
    # Detect Bangla using its Unicode block, avoiding an unavailable dependency.
    language = 'bn' if any('\u0980' <= char <= '\u09FF' for char in text) else 'en'
    speech=gTTS(text=text, lang=language, slow=False)
    audio_buffer=io.BytesIO()
    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

def quiz_generator(image, difficulty):
    prompt=f"""
    Generate 5 quiz questions based on the following text. 
    The questions should be of {difficulty} level.Also answer key should be provided for each question.
    """
    response=client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[image,prompt]
    )
    return response.text
