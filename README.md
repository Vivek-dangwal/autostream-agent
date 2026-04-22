# AutoStream: Social-to-Lead Agentic Workflow

This project is an AI-powered lead generation agent for **AutoStream**, built for the ServiceHive internship assignment. [cite_start]It uses a stateful agentic workflow to identify user intent, retrieve pricing via RAG, and capture qualified leads[cite: 6, 14].

## 🚀 How to Run Locally
1. **Clone the repository.**
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Setup Environment:** Create a `.env` file and add your `GROQ_API_KEY`.
4. **Run the App:** `python app.py`

## 🏗️ Architecture Explanation
[cite_start]For this agent, I chose a **State-Machine Architecture** (simulated via LangGraph-style logic)[cite: 79, 91]. Unlike a linear chatbot, this agent uses a **'Decision-Loop'** approach. 

1. [cite_start]**Intent Identification**: Every user input is first passed through an LLM classifier to determine if the user is seeking information or showing high purchase intent [cite: 19-23].
2. **RAG Integration**: If an inquiry is detected, the agent fetches specific data from a local `knowledge.json` file. [cite_start]This ensures the response is grounded in factual pricing data, preventing hallucinations [cite: 24-27].
3. **Stateful Lead Funnel**: When 'High-Intent' is detected, the agent enters a 'Locked-State.' [cite_start]It uses an entity extraction prompt to pull the user's Name, Email, and Platform [cite: 44-50]. 
4. **Gated Tool Execution**: The `mock_lead_capture` function is strictly gated. [cite_start]It will only trigger once the state dictionary contains all three required values, ensuring zero premature tool calls[cite: 51, 55].

[cite_start]I chose this architecture because it is robust, easy to scale into a full LangGraph implementation, and provides a clear separation between reasoning and action[cite: 79, 120].

## 📱 WhatsApp Integration
To deploy this agent on WhatsApp, I would use the following workflow:
1. [cite_start]**Webhook Setup**: Use a framework like FastAPI to create a webhook endpoint that listens for incoming messages from the **WhatsApp Business API** (via Twilio or Meta)[cite: 107].
2. **Session Management**: I would use the user's phone number as a unique `thread_id` to maintain their `user_state` (name, email, and progress) in a database like Redis.
3. **Response Loop**: When a user messages, the webhook triggers the `run_agent` logic. [cite_start]The AI's response is then sent back to the user's phone number using a POST request to the WhatsApp API[cite: 107].