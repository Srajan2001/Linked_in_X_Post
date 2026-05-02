import json

def load_profile():
    with open("D:\linkend_in_ai\linkedin_ai_agent\memory\profile.json", "r") as f:
        return json.load(f)
