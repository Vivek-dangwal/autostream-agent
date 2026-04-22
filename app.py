import os
import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# 1. INITIALIZATION
load_dotenv()
llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")

# 2. STATE MANAGEMENT
user_state = {
    "name": None,
    "email": None,
    "platform": None,
    "intent_locked": False
}

# 3. KNOWLEDGE RETRIEVAL (Section 3.2)
def get_rag_context():
    try:
        base_path = os.path.dirname(__file__)
        with open(os.path.join(base_path, "knowledge.json"), "r") as f:
            return json.dumps(json.load(f))
    except:
        return json.dumps({"pricing": {"Basic": "$29 (10 videos)", "Pro": "$79 (Unlimited, 4K)"}})

# 4. MOCK TOOL (Section 3.3)
def mock_lead_capture(name, email, platform):
    print(f"Lead captured successfully: {name}, {email}, {platform}")
    return f"### ✅ Success!\n**{name}**, your lead for **{platform}** is captured. We'll contact you at **{email}**."

# 5. CORE AGENTIC LOGIC
def run_agent(user_input):
    global user_state
    
    # --- PHASE 1: HARD-CODED DATA COLLECTION ---
    if user_state["intent_locked"]:
        
        # A. If we need a NAME and we don't have it yet, take the WHOLE input as the name
        if not user_state["name"]:
            # Simple check to make sure they didn't just say "hi"
            if len(user_input.split()) <= 4: 
                user_state["name"] = user_input.strip()
            else:
                # If it's a long sentence, let the LLM try to find the name
                res = llm.invoke(f"Extract the person's name from: '{user_input}'. Return ONLY the name.").content
                user_state["name"] = res.strip()
            return f"Thanks, {user_state['name']}! What is your **email address**?"

        # B. If we need an EMAIL, look for the @ symbol
        if not user_state["email"]:
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', user_input)
            if emails:
                user_state["email"] = emails[0]
                return "Got it! Which **platform** do you primarily use (YouTube, Instagram, or Facebook)?"
            else:
                return "Please provide a valid email address so we can reach you."

        # C. If we need a PLATFORM
        if not user_state["platform"]:
            platforms = ["youtube", "instagram", "facebook", "tiktok"]
            for p in platforms:
                if p in user_input.lower():
                    user_state["platform"] = p.capitalize()
                    break
            if not user_state["platform"]:
                user_state["platform"] = user_input.strip() # Fallback

        # D. TRIGGER SUCCESS
        result = mock_lead_capture(user_state["name"], user_state["email"], user_state["platform"])
        user_state.update({"name": None, "email": None, "platform": None, "intent_locked": False})
        return result

    # --- PHASE 2: INTENT DETECTION ---
    user_input_l = user_input.lower()
    
    # Check for High-Intent (Sign up)
    if any(x in user_input_l for x in ["sign up", "try pro", "subscribe", "want pro", "get started"]):
        user_state["intent_locked"] = True
        return "I'd love to help you sign up for AutoStream! What is your **full name**?"

    # Check for Pricing (RAG)
    if any(x in user_input_l for x in ["price", "cost", "plan", "pricing"]):
        context = get_rag_context()
        prompt = f"Use this context: {context}. List AutoStream pricing ($29 and $79) in a clear bulleted list."
        return llm.invoke(prompt).content

    return "Hello! I'm the AutoStream Assistant. I can help with **pricing** or **signing up**. How can I help?"

if __name__ == "__main__":
    while True:
        msg = input("User: ")
        if msg.lower() in ["exit", "quit"]: break
        print(f"Agent: {run_agent(msg)}")