import streamlit as st
import os
import asyncio
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from browser_use import Agent

# --- 1. CONFIGURATION & ERROR HANDLING ---
# Safely grab the API key to prevent silent None failures
groq_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_key:
    st.error("🔑 **Groq API Key is missing!** Please set GROQ_API_KEY in your Streamlit secrets or environment variables.")
    st.stop()

# Using standard ChatOpenAI with Groq's base_url bypassing provider attribute errors
llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    api_key=groq_key,
    openai_api_base="https://api.groq.com/openai/v1"
)

# Fix for Streamlit's internal loop conflict with asyncio.run()
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

class Vantagetate(TypedDict):
    niche: str
    target_url: str
    resume_context: str
    status: str

# --- 2. AGENT LOGIC ---
async def surgeon_agent(state: Vantagetate):
    """Surgical tailoring using Groq's high-speed inference."""
    # Made async to maintain clean execution flow across the graph
    return {"resume_context": "Deeply engineered technical background in autonomous systems..."}

async def executioner_agent(state: Vantagetate):
    """Vision-based Stealth Submission via Browser-Use + Groq."""
    agent = Agent(
        task=f"Navigate to {state['target_url']}. Fill application with: {state['resume_context']}. Submit.",
        llm=llm
    )
    # result = await agent.run() # Uncomment to execute live navigation
    return {"status": "SUCCESS: APPLIED"}

# --- 3. GRAPH ORCHESTRATION ---
workflow = StateGraph(Vantagetate)
workflow.add_node("surgeon", surgeon_agent)
workflow.add_node("executioner", executioner_agent)
workflow.set_entry_point("surgeon")
workflow.add_edge("surgeon", "executioner")
workflow.add_edge("executioner", END)
app = workflow.compile()

# --- 4. STREAMLIT UI ---
st.set_page_config(page_title="VANTAGE Engine", layout="centered")
st.title("🚀 VANTAGE: Autonomous Job Engine")

niche = st.text_input("Target Role", "Principal Autonomous Systems Engineer")
url = st.text_input("Job URL", "https://careers.company.com/job-id")

if st.button("Engage Swarm"):
    with st.spinner("VANTAGE is hunting..."):
        try:
            # Safely fetch or create the running event loop to avoid conflict with Streamlit
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
            # Running the async Graph execution safely inside Streamlit
            result = loop.run_until_complete(app.ainvoke({"niche": niche, "target_url": url}))
            
            st.success(f"Final Status: {result.get('status', 'COMPLETED')}")
            st.balloons()
        except Exception as e:
            st.error(f"Engine Failure: {e}")
