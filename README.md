# 🌆 AetherCity: Human-in-the-Loop Agentic Urban Intelligence

[Python Version](https://www.python.org/) ([image](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg))
[LangChain](https://python.langchain.com/) ([image](https://img.shields.io/badge/Orchestration-LangChain-green.svg))
[LLM: Mistral AI](https://mistral.ai/) ([image](https://img.shields.io/badge/LLM-Mistral%20AI-orange.svg))
[Search: Tavily](https://tavily.com/) ([image](https://img.shields.io/badge/Search-Tavily%20API-lightblue.svg))
[Weather: OpenWeather](https://openweathermap.org/) ([image](https://img.shields.io/badge/Telemetry-OpenWeatherMap-yellow.svg))
[UI: Streamlit](https://streamlit.io/) ([image](https://img.shields.io/badge/Interface-Streamlit-red.svg))
[License: MIT](LICENSE) ([image](https://img.shields.io/badge/License-MIT-purple.svg))

An agentic conversational system designed for real-time city telemetry, localized news synthesis, and general reasoning. Built with **LangChain**, **Mistral AI**, **OpenWeatherMap**, **Tavily**, and **Streamlit**, featuring strict **Human-in-the-Loop (HITL) Guardrails** for secure external tool execution.

---

## 🏛️ System Architecture

```text
                         [ User Query ]
                               │
                               ▼
                ┌──────────────────────────────┐
                │  Mistral LLM Reasoning Core  │
                │      (Tool Call Intent)      │
                └──────────────┬───────────────┘
                               │
                               ▼
               ┌────────────────────────────────┐
               │   🛡️ HITL Security Guardrail   │
               │   (Manual User Authorization)  │
               └───────┬────────────────┬───────┘
                       │                │
              [ Authorized ]       [ Denied ]
                       ▼                ▼
         ┌─────────────────────────┐  ┌─────────────────────────┐
         │ External Tool Invocations│  │  Intercepted Execution  │
         │ ├─ OpenWeatherMap API   │  │   (Tool Denied Message) │
         │ └─ Tavily News Search   │  └────────────┬────────────┘
         └─────────────┬───────────┘               │
                       │ Payload                   │
                       └───────────────┬───────────┘
                                       ▼
                        ┌─────────────────────────────┐
                        │ Final Grounded Synthesis    │
                        └─────────────────────────────┘
```

---

## ✨ Key Technical Highlights

- **Autonomous Tool Binding & Intent Detection:** Uses Mistral function calling to determine when to trigger telemetry or search tools versus answering from parametric memory.
- **Human-in-the-Loop (HITL) Guardrails:** Intercepts agent tool execution in both CLI and Streamlit interfaces, requiring manual user authorization before performing external network actions.
- **Dual Interface Support:** Includes an interactive Streamlit UI with telemetry sidebars and a fast, headless terminal CLI.
- **Graceful Degradation:** Handles missing API keys, rate limits, and network connection drops cleanly without breaking the conversational context.

---

## 📂 Repository Structure

```text
├── .env.example        # Environment variable template
├── .gitignore          # Git exclusion rules
├── app.py              # Streamlit web application with HITL state management
├── main.py             # Headless terminal CLI agent with middleware approval
├── LICENSE              # Project distribution license (MIT)
├── requirements.txt    # Pinned Python dependencies
├── DECISIONS.md        # Architecture decisions, trade-offs & guardrail scope
└── README.md           # Master documentation & quickstart
```

---

## 🚀 Quickstart

### 1. Clone & Setup Virtual Environment

```bash
git clone https://github.com/Aditya-C-Patil/AetherCity.git
cd AetherCity

python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Run the Application

**Interactive Streamlit Web Hub:**

```bash
streamlit run app.py
```

**Terminal CLI Agent:**

```bash
python main.py
```
