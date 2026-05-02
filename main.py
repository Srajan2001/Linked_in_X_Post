from agents.profile_agent import load_profile
from agents.trend_agent import fetch_trend
from agents.post_writer_agent import generate_linkedin_post, revise_linkedin_post
from agents.approval_agent import approve_post
from agents.memory_agent import retrieve_past_posts
from agents.router_agent import route_content
from agents.critic_agent import evaluate_draft # Import the Critic

profile = load_profile()
trend = fetch_trend() 

print(f"Checking long-term memory for past posts about {trend['topic']}...")
past_posts = retrieve_past_posts(trend['topic'])

print(f" Generating initial post...")
current_post = generate_linkedin_post(profile, trend, past_examples=past_posts)

# --- NEW: The AI Self-Correction Loop ---
max_revisions = 3 # Prevent an infinite loop if the AI gets stuck
revision_count = 0

while revision_count < max_revisions:
    is_approved, critic_feedback = evaluate_draft(current_post)
    
    if is_approved:
        print(" Critic approved the draft!")
        break
    else:
        print(f" Critic rejected draft. Reason: {critic_feedback}")
        print("Sending back to Writer Agent for revisions...")
        current_post = revise_linkedin_post(current_post, critic_feedback)
        revision_count += 1

# --- Your original Human Approval Loop ---
while True:
    status, human_feedback = approve_post(current_post, trend['topic'])
    
    if status == "approved":
        print("\nCommencing Omnichannel Routing...")
        route_content(current_post, platform="twitter")
        route_content(current_post, platform="email")
        print("\nAll tasks complete. Pipeline finished.")
        break
    elif status == "edit":
        print(f"\nRevising post based on your feedback: '{human_feedback}'...")
        current_post = revise_linkedin_post(current_post, human_feedback)
    else:
        break