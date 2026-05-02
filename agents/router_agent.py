import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure the output directory exists
os.makedirs("outputs", exist_ok=True)

def route_content(approved_post, platform="twitter"):
    print(f"\n Routing content to {platform.upper()} (Strict JSON)...")
    
    if platform.lower() == "twitter":
        instructions = """
        Convert the provided LinkedIn post into a highly engaging Twitter/X thread.
        RULES:
        1. Break the content into 3 to 5 separate tweets.
        2. Keep each tweet strictly under 280 characters.
        3. Make the tone punchier and more direct than the LinkedIn version.
        
        You MUST return a strict JSON object with this exact schema:
        {
            "tweet_1": "Text for the first tweet...",
            "tweet_2": "Text for the second tweet...",
            "tweet_3": "Text for the third tweet..."
        }
        """
    elif platform.lower() == "email":
        instructions = """
        Convert the provided LinkedIn post into a short, casual email update.
        RULES:
        1. Keep the body under 4 sentences.
        2. Remove all emojis and hashtags.
        3. Make it sound like a quick note sent to a colleague.
        
        You MUST return a strict JSON object with this exact schema:
        {
            "subject": "A catchy email subject line",
            "body": "The plain text body of the email..."
        }
        """
    else:
        return None

    prompt = f"""
    {instructions}
    
    ORIGINAL APPROVED POST:
    {approved_post}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" }, # 🔥 THIS IS THE MAGIC BULLET 🔥
            messages=[
                {"role": "system", "content": "You are a precise data transformation agent that ONLY outputs valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Parse the JSON string back into a Python dictionary
        structured_data = json.loads(response.choices[0].message.content)
        
        # Save the raw JSON to a file for record keeping
        file_path = f"outputs/{platform}_post.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(structured_data, f, indent=4)
            
        print(f"Successfully created {platform} JSON!")
        return structured_data
        
    except Exception as e:
        print(f"Error routing content: {str(e)}")
        return None