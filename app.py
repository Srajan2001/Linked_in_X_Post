import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
from agents.trend_agent import fetch_trend
from agents.post_writer_agent import generate_linkedin_post, revise_linkedin_post
from agents.critic_agent import evaluate_draft
from agents.memory_agent import retrieve_past_posts, save_to_memory
from agents.router_agent import route_content
from agents.image_agent import generate_post_image

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Content Agent", layout="wide", page_icon="🤖")
st.title("Enterprise AI Content Pipeline")

# --- SESSION STATE INITIALIZATION ---
if "step" not in st.session_state: st.session_state.step = 1
if "news_data" not in st.session_state: st.session_state.news_data = []
if "news_limit" not in st.session_state: st.session_state.news_limit = 5
if "news_refreshes" not in st.session_state: st.session_state.news_refreshes = 0
if "current_draft" not in st.session_state: st.session_state.current_draft = ""
if "current_topic" not in st.session_state: st.session_state.current_topic = ""
if "trend_payload" not in st.session_state: st.session_state.trend_payload = {}

# --- SIDEBAR: DYNAMIC USER INPUTS ---
with st.sidebar:
    st.header(" Agent Controls")
    
    st.subheader("1. Your Profile")
    user_name = st.text_input("Name", value="", placeholder="e.g. Srajan")
    roles = ["Data Analyst", "Data Scientist", "Software Engineer", "Product Manager", "Founder"]
    user_role = st.selectbox("Role", options=roles, index=None, placeholder="Select your role...")
    common_skills = ["Python", "SQL", "Power BI", "Tableau", "AWS", "Machine Learning", "PySpark"]
    user_skills = st.multiselect("Core Skills", options=common_skills, default=None)
    
    st.subheader("2. Content Strategy")
    user_topic = st.text_input("Topic", value="", placeholder="e.g. AI in Data Analytics")
    target_audience = st.selectbox("Target Audience", ["Peers & Industry Experts", "Recruiters", "Beginners"], index=0)
    post_tone = st.selectbox("Content Tone", ["Professional", "Bold & Provocative", "Storytelling"], index=0)
    use_live_search = st.toggle(" Fetch Live News", value=True)

    ready_to_research = user_name and user_role and user_skills and user_topic
    # --- NEW: Dynamic Button Label ---
    button_text = " Fetch News & Research" if use_live_search else "🚀 Generate Post"

    # --- STEP 1 TRIGGER ---
    # FIX: We added key="main_action_btn" right after the button_text!
    if st.button(button_text, key="main_action_btn", use_container_width=True, type="primary", disabled=not ready_to_research):
        # Save profile to session state so we can use it in later steps
        st.session_state.profile = {
            "name": user_name, "role": user_role, "skills": user_skills, 
            "audience": target_audience, "tone": post_tone
        }
        st.session_state.current_topic = user_topic
        st.session_state.current_draft = "" # Reset any old drafts
        st.session_state.use_live_search = use_live_search # Save toggle state
        
        if use_live_search:
            with st.spinner(" Scraping 15 latest articles..."):
                st.session_state.news_data = fetch_trend(topic_keyword=user_topic, max_results=15)
            st.session_state.news_limit = 5
            st.session_state.news_refreshes = 0
            st.session_state.step = 2 # Move to selection phase
        else:
            st.session_state.trend_payload = {"topic": user_topic, "live_context": ""}
            st.session_state.step = 3 # Skip straight to drafting
        st.rerun()

# --- MAIN DASHBOARD: STEP 2 (NEWS SELECTION) ---
if st.session_state.step == 2:
    st.subheader("Step 2: Curate Your News Context")
    st.info("Read the articles below. Check the boxes for the ones you want the AI to read before writing.")
    
    selected_articles = []
    displayed_news = st.session_state.news_data[:st.session_state.news_limit]
    
    for idx, article in enumerate(displayed_news):
        # Create a clean UI for each article
        st.markdown(f"#### [{article.get('title')}]({article.get('href')})")
        st.caption(f"{article.get('body')[:200]}...") # Show snippet
        
        # Checkbox for selection
        if st.checkbox(" Include this in AI Context", key=f"news_check_{idx}"):
            selected_articles.append(article)
        st.divider()
        
    # Navigation Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.news_refreshes < 2 and len(st.session_state.news_data) > st.session_state.news_limit:
            if st.button(" Load 5 More Articles"):
                st.session_state.news_limit += 5
                st.session_state.news_refreshes += 1
                st.rerun()
                
    with col2:
        if st.button("Step 3: Generate Post", type="primary"):
            # Compile only the checked articles!
            formatted_context = "\n\n".join([f"- {a['title']}: {a['body']}" for a in selected_articles])
            
            st.session_state.trend_payload = {
                "topic": st.session_state.current_topic,
                "live_context": formatted_context
            }
            st.session_state.step = 3 # Move to Drafting
            st.rerun()

# --- MAIN DASHBOARD: STEP 3 (DRAFTING & ROUTING) ---
if st.session_state.step == 3:
    st.subheader(f"Step 3: Review Draft - {st.session_state.current_topic}")
    
    # 1. Draft Generation 
    if not st.session_state.current_draft:
        
        # --- DYNAMIC ROUTING LOGIC ---
        if st.session_state.get("use_live_search", True):
            selected_model = "gpt-4o-mini"
            selected_tokens = 450
            spinner_text = " Synthesizing news and drafting post (GPT-4o-mini)..."
        else:
            selected_model = "gpt-4o"
            selected_tokens = 700
            spinner_text = " Utilizing deep expertise to draft post (GPT-4o)..."
            
        with st.spinner(spinner_text):
            past_posts = retrieve_past_posts(st.session_state.current_topic)
            
            draft = generate_linkedin_post(
                st.session_state.profile, 
                st.session_state.trend_payload, 
                past_examples=past_posts,
                model=selected_model,
                max_tokens=selected_tokens
            )
            
            for i in range(3): # Critic Loop
                is_approved, feedback = evaluate_draft(draft)
                if is_approved: break
                draft = revise_linkedin_post(draft, feedback)
                
            st.session_state.current_draft = draft
            st.rerun() 
            
    # 2. Text Editor & AI Edits (This is what was missing!)
    edited_draft = st.text_area("Your LinkedIn Post", st.session_state.current_draft, height=300)
    
    st.markdown("** AI Quick Edits:**")
    colA, colB, colC = st.columns(3)
    if colA.button("Make it Shorter"):
        with st.spinner("Rewriting..."):
            st.session_state.current_draft = revise_linkedin_post(edited_draft, "Make this post 25% shorter.")
            st.rerun()
    if colB.button("Make it More Technical"):
        with st.spinner("Rewriting..."):
            st.session_state.current_draft = revise_linkedin_post(edited_draft, "Increase the technical depth.")
            st.rerun()
    if colC.button("Add a Call to Action"):
        with st.spinner("Rewriting..."):
            st.session_state.current_draft = revise_linkedin_post(edited_draft, "Add a question at the end.")
            st.rerun()

    st.divider()
    
    # 3. Final Approval & Routing
    if st.button(" Approve & Route to Omnichannel", type="primary"):
        with st.spinner(" Routing content & rendering images..."):
            save_to_memory(edited_draft, st.session_state.current_topic)
            twitter_data = route_content(edited_draft, platform="twitter")
            email_data = route_content(edited_draft, platform="email")
            generated_image_url = generate_post_image(edited_draft)
            
            st.success(" Pipeline Complete! Ready to Publish.")
            st.divider()
            
            # --- ROW 1: THE MAIN LINKEDIN POST ---
            st.subheader("🟦 LinkedIn Post")
            st.code(edited_draft, language="markdown")
            st.link_button(" Open LinkedIn to Post", "https://www.linkedin.com/feed/", use_container_width=True)
            
            st.divider()
            
            # --- ROW 2: OMNICHANNEL & GRAPHICS ---
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("Twitter / X")
                if twitter_data:
                    full_thread = "\n\n".join(twitter_data.values())
                    st.info(full_thread)
                    
                    encoded_tweet = urllib.parse.quote(full_thread)
                    twitter_url = f"https://twitter.com/intent/tweet?text={encoded_tweet}"
                    st.link_button(" Draft on X", twitter_url, type="primary", use_container_width=True)
            
            with col2:
                st.subheader("Email")
                if email_data:
                    st.markdown(f"**Subject:** {email_data.get('subject', '')}")
                    st.info(email_data.get('body', ''))
            
            with col3:
                st.subheader("Graphic")
                if generated_image_url:
                    try:
                        img_response = requests.get(generated_image_url, timeout=15)
                        if img_response.status_code == 200:
                            img_bytes = img_response.content
                            img = Image.open(BytesIO(img_bytes))
                            st.image(img, use_container_width=True)
                            
                            st.download_button(
                                label="⬇Download Image",
                                data=img_bytes,
                                file_name=f"{st.session_state.current_topic.replace(' ', '_')}_graphic.png",
                                mime="image/png",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error("Failed to load image preview.")