import os
import urllib.parse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post_image(approved_post):
    print("\nImage Agent is designing a custom graphic...")
    
    # 1. Ask the LLM to read the post and design a visual concept
    prompt = f"""
    You are an expert graphic designer for LinkedIn.
    Read the following post and write a highly detailed, 1-sentence image generation prompt.
    The image should be professional, minimalistic, and use modern corporate illustration styles (like isometric 3D or clean vector art).
    Do NOT include text or words in the image prompt.
    
    POST:
    {approved_post}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You only output the 1-sentence image prompt. No other text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        image_prompt = response.choices[0].message.content.strip()
        print(f"Generated Image Concept: {image_prompt}")
        
        # 2. URL-encode the prompt so it can be sent via an HTTP request
        encoded_prompt = urllib.parse.quote(image_prompt)
        
        # 3. Use the free Pollinations AI endpoint (No API key needed!)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true"
        
        print(" Image generated successfully!")
        return image_url
        
    except Exception as e:
        print(f"Image Agent Error: {str(e)}")
        return None