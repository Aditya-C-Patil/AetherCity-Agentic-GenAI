# 🌆 AetherCity · Human-in-the-Loop Agentic GenAI Assistant

AetherCity is an interactive conversational AI system built with **LangChain**, **Mistral AI (`mistral-small-2506`)**, **OpenWeatherMap API**, and **Tavily AI Search**. The project includes an interactive **Streamlit** chat interface with dynamic human-in-the-loop (HITL) approval buttons and a terminal-based conversational agent with middleware approval gates.

The system serves as a conversational assistant for general inquiries and conditionally activates external tools only when real-time city weather telemetry or local breaking news is requested, requiring human confirmation before querying external APIs.

---

## 🏗️ Architecture & Interaction Flow

The assistant routes general queries directly to the LLM and triggers tool calling with an authorization checkpoint only when external city data is needed:

```text
                           ┌────────────────────────┐
                           │   User Chat Message    │
                           └───────────┬────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. LLM Intent Classification & Tool Binding                                 │
│    • Model: ChatMistralAI (`mistral-small-2506`)                            │
│    • General Inquiries: Responds directly without calling tools             │
│    • Weather / News Queries: Formulates tool call parameters                │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                     ┌─────────────────┴─────────────────┐
       [ General Query ]                     [ Tool Call Required ]
                     │                                   │
                     │                                   ▼
                     │       ┌────────────────────────────────────────────────┐
                     │       │ 2. Human-in-the-Loop (HITL) Approval Checkpoint│
                     │       │    • Streamlit UI: "Authorize" vs "Deny"       │
                     │       │    • CLI: Terminal prompt `(yes/no)`           │
                     │       └───────────────────┬────────────────────────────┘
                     │                           │
                     │             ┌─────────────┴─────────────┐
                     │  [ Approved ]                          [ Denied ]
                     │             ▼                           ▼
                     │  ┌───────────────────────┐   ┌─────────────────────────┐
                     │  │ 3. Execute Tool       │   │ Return Rejection Message│
                     │  │  • `get_weather`      │   │ ("Tool call denied")    │
                     │  │  • `get_news`         │   └────────────┬────────────┘
                     │  └──────────┬────────────┘                │
                     │             │                             │
                     │             └─────────────┬───────────────┘
                     │                           │
                     ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. LLM Synthesis & Response Delivery                                        │
│    • Streamlit Chat: Appends final message to conversation state            │
│    • CLI Terminal: Prints assistant response                                │
└─────────────────────────────────────────────────────────────────────────────┘
```
## **📁 Repository Structure**
```text
├── app.py              # Streamlit web application with HITL approval cards
├── main.py             # CLI terminal agent with wrap_tool_call middleware
├── requirements.txt    # Python package dependencies
├── .env.example        # Environment variable template for required API keys
├── .gitignore          # Git ignore rules for virtual environments and credentials
└── README.md           # Project documentation
