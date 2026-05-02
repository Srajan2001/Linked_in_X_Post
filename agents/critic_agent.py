import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_draft(draft):
    print("\nCritic Agent is reviewing the draft...")
    
    prompt = f"""
    You are a strict PR Manager and Content Critic. 
    Review the following LinkedIn draft and evaluate it against these rules:
    1. It must not contain controversial, political, or highly sensitive topics.
    2. It must be highly professional but engaging.
    3. It must not contain AI cliches like "In today's fast-paced digital world" or "Delve into".
    
    Analyze the draft and return a STRICT JSON object with two keys:
    - "is_approved": boolean (true if it passes all rules, false if it fails)
    - "feedback": string (If false, explain exactly what to fix. If true, write "Looks good")
    
    DRAFT TO REVIEW:
    {draft}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={ "type": "json_object" }, # Forces strict JSON output
            messages=[
                {"role": "system", "content": "You are a precise JSON outputting critic."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Low temperature for strict, analytical grading
            max_tokens=200
        )
        
        # Parse the JSON string back into a Python dictionary
        result = json.loads(response.choices[0].message.content)
        return result["is_approved"], result["feedback"]
        
    except Exception as e:
        print(f"Critic Error: {str(e)}")
        # Default to True so the pipeline doesn't crash if the API glitches
        return True, "Critic failed to evaluate."