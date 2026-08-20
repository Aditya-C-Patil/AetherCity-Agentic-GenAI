# 🌆 AetherCity · Agentic GenAI Urban Intelligence & Conversational Assistant

AetherCity is an interactive AI assistant powered by **LangChain**, **Mistral AI (`mistral-small-2506`)**, **OpenWeatherMap API**, and **Tavily AI Search**. The project includes an interactive **Streamlit** chat interface with dynamic human-in-the-loop (HITL) approval buttons and a terminal-based conversational agent with middleware approval gates.

The agent answers city-specific questions, fetches real-time temperature and weather conditions, and pulls breaking local news—requesting human confirmation before executing any external tool.

---

## 🏗️ Architecture & Interaction Flow

The assistant uses tool calling with a human approval checkpoint before any external API is queried:

```text
                           ┌────────────────────────┐
                           │   User Chat Message    │
                           │ (e.g., "Weather in IN")│
                           └───────────┬────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. LLM Tool Selection & Reasoning                                           │
│    • Model: ChatMistralAI (`mistral-small-2506`)                            │
│    • Checks query intent and prepares tool call arguments                   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. Human-in-the-Loop (HITL) Approval Checkpoint                             │
│    • Streamlit UI: "Approve Tool Call" vs "Deny Tool Call" buttons          │
│    • CLI: Interactive terminal middleware confirmation (`(yes/no)`)         │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                     ┌─────────────────┴─────────────────┐
            [ Approved ]                                [ Denied ]
                     ▼                                      ▼
┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
│ 3. Tool Execution                    │  │ Return Rejection ToolMessage      │
│  • `get_weather` (OpenWeatherMap API)│  │ ("Tool call denied by user.")     │
│  • `get_news` (Tavily Search API)    │  └─────────────────┬─────────────────┘
└──────────────────┬───────────────────┘                    │
                   │                                        │
                   └───────────────────┬────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. LLM Synthesis & Response Delivery                                        │
│    • Ingests tool outputs / denial status                                   │
│    • Generates final conversational response for the user                   │
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
