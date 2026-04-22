import streamlit as st
from app import run_agent, user_state

# 1. Page Configuration
st.set_page_config(page_title="AutoStream | Vivek Dangwal", page_icon="📈", layout="wide")

# 2. Brand-Inspired CSS (YouTube Red, Instagram Purple, Facebook Blue)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #060709;
        color: #e6edf3;
    }
    
    /* Sidebar: Facebook Blue & Instagram Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1877F2 0%, #833AB4 100%);
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* YouTube Red Accents */
    .stButton>button {
        background-color: #FF0000;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }

    /* Professional Header */
    .main-header {
        background: rgba(255, 255, 255, 0.03);
        padding: 30px;
        border-radius: 20px;
        border-left: 5px solid #FF0000;
        margin-bottom: 25px;
    }

    /* Robo-Chat Bubbles with Glow */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background: rgba(24, 119, 242, 0.1) !important;
        border: 1px solid #1877F2;
        box-shadow: 0 0 15px rgba(24, 119, 242, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar: Lead Tracker
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3670/3670147.png", width=80) # YouTube-style play icon
    st.title("Lead Tracker")
    st.markdown("---")
    
    # State Monitor with Brand Colors 
    for key, val in user_state.items():
        label = key.replace("_", " ").title()
        icon = "🟢" if val else "⚪"
        st.markdown(f"### {icon} {label}")
        st.code(val if val else "Waiting for data...")
    
    st.markdown("---")
    if st.button("RESET PIPELINE"):
        user_state.update({"name": None, "email": None, "platform": None, "intent_locked": False})
        st.session_state.messages = []
        st.rerun()

# 4. Main UI Content
st.markdown("""
    <div class="main-header">
        <h1 style='margin:0; font-size: 3rem;'>AutoStream</h1>
        <h3 style='margin:0; color:#8b949e; font-weight: 400;'>Agentic Lead Workflow by <b>Vivek Dangwal</b></h3>
    </div>
""", unsafe_allow_html=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "System online. Ready to capture high-intent leads across **YouTube**, **Instagram**, and **Facebook**. How can I help?"}]

for message in st.session_state.messages:
    # Custom avatars for YouTube/FB feel
    avatar = "https://cdn-icons-png.flaticon.com/512/4712/4712139.png" if message["role"] == "assistant" else "https://cdn-icons-png.flaticon.com/512/1144/1144760.png"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Interaction
if prompt := st.chat_input("Enter message (e.g., 'What is the Pro plan cost?')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="https://cdn-icons-png.flaticon.com/512/1144/1144760.png"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="https://cdn-icons-png.flaticon.com/512/4712/4712139.png"):
        with st.spinner("Processing Agentic Reasoning..."):
            response = run_agent(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()