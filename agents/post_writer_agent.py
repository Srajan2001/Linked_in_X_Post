import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Added model and max_tokens as configurable parameters
def generate_linkedin_post(profile_data, trend_data, past_examples="", model="gpt-4o-mini", max_tokens=450):
    print(f"\nWriter Agent booting up with model: {model} (Tokens: {max_tokens})")
    
    prompt = f"""
    You are an expert LinkedIn ghostwriter. 
    Write a highly engaging LinkedIn post about: {trend_data['topic']}.
    
    Here is the latest breaking news on this topic to include (if any):
    {trend_data.get('live_context', 'No recent news provided. Rely on your deep expertise to write a highly insightful, thought-leadership post.')}
    
    THE STRATEGY:
    - Author Name: {profile_data.get('name')}
    - Author Role: {profile_data.get('role')}
    - Core Skills to weave in naturally: {', '.join(profile_data.get('skills', []))}
    - Target Audience: {profile_data.get('audience', 'General Professionals')}
    - Requested Tone: {profile_data.get('tone', 'Professional')}
    
    INSTRUCTIONS FOR TONE CLONING:
    Below are examples of the user's past successful LinkedIn posts. 
    Mimic this exact style in your new post. If no examples are provided, strictly follow the "Requested Tone" above.
    
    PAST EXAMPLES:
    {past_examples}
    
    CRITICAL INSTRUCTION: Output ONLY the final LinkedIn post. Do NOT include any introductory or concluding remarks.
    """

    try:
        response = client.chat.completions.create(
            model=model, # Dynamic Model
            messages=[
                {"role": "system", "content": "You are an AI LinkedIn content strategist. You only output final post copy."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens # Dynamic Token Limit
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating post: {str(e)}"

def revise_linkedin_post(draft, feedback):
    prompt = f"""
    You are an expert LinkedIn ghostwriter. 
    The user provided feedback on a recent draft.
    
    Original Draft:
    {draft}
    
    User Feedback:
    {feedback}
    
    Rewrite the post applying the feedback exactly. Ensure it remains highly engaging and professional.
    Output ONLY the revised draft.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Revisions can stay cheap
            messages=[
                {"role": "system", "content": "You are an AI LinkedIn content strategist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating revision: {str(e)}"