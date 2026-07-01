# SNYAPSE FLOW

SNYAPSE FLOW is an autonomous, multi-agent swarm engine designed to hunt for high-growth job opportunities, semantically tailor resume artifacts using RAG, and execute stealthy applications via vision-guided browser automation.

## Architecture
- **Scout Agent:** High-frequency monitoring of job boards.
- **Surgeon Agent:** RAG-based logic for hyper-personalization.
- **Executioner Agent:** Vision-guided agentic browser for stealth navigation.

## Key Technologies
- **Orchestration:** LangGraph (Stateful, cyclic workflows)
- **Inference:** Groq LPU (GPT-OSS-120B reasoning)
- **Automation:** Browser-Use (Vision-language navigation)
- **Stealth:** Residential proxy integration & behavioral jitter

## Quickstart
1. Set your environment variables:
   `export GROQ_API_KEY='...'`
   `export RESIDENTIAL_PROXY_URL='...'`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the engine: `python main.py`
