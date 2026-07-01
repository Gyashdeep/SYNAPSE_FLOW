import streamlit as st
import os
import asyncio
from typing import TypedDict
from langgraph.graph import StateGraph, END

# --- DEPENDENCY HANDLING ---
# Patches Streamlit's runtime to handle nested async execution loops safely
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig

# --- 1. CONFIGURATION & CORE ENGINE SETUP ---
groq_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
proxy_url = st.secrets.get("RESIDENTIAL_PROXY_URL") or os.getenv("RESIDENTIAL_PROXY_URL")

if not groq_key:
    st.error("🔑 **Groq API Key is missing!** Provide it via environment variables or Streamlit secrets.")
    st.stop()

# Initialize Groq via standard OpenAI-compatible client wrapper
# This satisfies the structural and field-level validation checks of browser-use natively
llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    api_key=groq_key,
    base_url="https://api.groq.com/openai/v1"
)

# Configure Browser Automation with Proxy configurations if available
browser_config = BrowserConfig(
    headless=True,
    proxy={"server": proxy_url} if proxy_url else None
)
browser = Browser(config=browser_config)

# --- 2. STATE GRAPH DEFINITION ---
class SnyapseState(TypedDict):
    niche: str
    target_url: str
    resume_context: str
    status: str

# --- 3. AGENT NODE LOGIC ---
async def surgeon_agent(state: SnyapseState):
    """
    Surgeon Agent: Context optimization & Hyper-personalization node.
    """
    tailored_bio = (
        f"Deeply engineered technical background matching target domain: {state['niche']}. "
        f"Specialized in high-scale systems implementation."
    )
    return {"resume_context": tailored_bio, "status": "CONTEXT_SYNTHESIZED"}

async def executioner_agent(state: SnyapseState):
    """
    Executioner Agent: Vision-guided orchestration engine using browser-use.
    """
    task_instructions = (
        f"Navigate to {state['target_url']}. "
        f"Analyze the input form structure. Fill out information fields accurately using data: "
        f"{state['resume_context']}. Once completely filled out, trigger the submit or continue pipeline."
    )
    
    agent = Agent(
        task=task_instructions,
        llm=llm,
        browser=browser
    )
    
    try:
        # Run agentic visual navigation 
        await agent.run()
        execution_status = "SUCCESS: APPLICATION_EXECUTED"
    except Exception as browser_err:
        execution_status = f"FAILED: Browser Execution Interrupted ({str(browser_err)})"
    finally:
        await browser.close()
        
    return {"status": execution_status}

# --- 4. GRAPH ORCHESTRATION ---
workflow = StateGraph(SnyapseState)

# Append structural nodes to topology
workflow.add_node("surgeon", surgeon_agent)
workflow.add_node("executioner", executioner_agent)

# Set network edges & entry routing
workflow.set_entry_point("surgeon")
workflow.add_edge("surgeon", "executioner")
workflow.add_edge("executioner", END)

# Compile Execution Blueprint
app = workflow.compile()

# --- 5. STREAMLIT INTERFACE LAYER ---
st.set_page_config(page_title="SNYAPSE FLOW", layout="centered")
st.title("🚀 SNYAPSE FLOW: Autonomous Swarm Engine")
st.caption("Stateful, multi-agent automation platform powered by Groq LPU & Browser-Use.")

niche = st.text_input("Target Domain / Role", "Principal Autonomous Systems Engineer")
url = st.text_input("Target Application URL", "https://careers.company.com/job-id")

if st.button("Engage Swarm"):
    if not url or url == "https://careers.company.com/job-id":
        st.warning("Please provide a valid Target Application URL.")
    else:
        with st.spinner("SNYAPSE swarm vectors hunting context..."):
            try:
                # Thread Loop Management within Streamlit architecture context
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                # Run Multi-Agent Blueprint asynchronously
                initial_state = {"niche": niche, "target_url": url, "resume_context": "", "status": "INIT"}
                result = loop.run_until_complete(app.ainvoke(initial_state))
                
                # Interface telemetry output
                final_status = result.get("status", "COMPLETED")
                if "SUCCESS" in final_status:
                    st.success(f"Execution Target Reached: {final_status}")
                    st.balloons()
                else:
                    st.error(f"Execution Log: {final_status}")
                    
            except Exception as e:
                st.error(f"Swarm Fatal Engine Failure: {e}")
