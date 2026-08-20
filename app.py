import os
import requests
import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from tavily import TavilyClient

# Load environment variables from local .env
load_dotenv()

# =========================================================
# ⚙️ Page Configuration & Custom Theme
# =========================================================
st.set_page_config(
    page_title="AetherCity · Agentic GenAI Assistant",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ⚙️ Sidebar: Telemetry Configuration & Safeguards
# =========================================================
with st.sidebar:
    st.markdown("### 🌆 AetherCity Control Hub")
    st.caption("Agentic GenAI Telemetry & Safeguards")
    
    st.markdown("Configure API credentials below or leverage local `.env` keys:")
    
    input_mistral = st.text_input(
        "Mistral API Key",
        type="password",
        placeholder="Enter key or use .env",
        help="Required for core Mistral LLM reasoning"
    )
    input_weather = st.text_input(
        "OpenWeather API Key",
        type="password",
        placeholder="Enter key or use .env",
        help="Required for real-time weather & telemetry extraction"
    )
    input_tavily = st.text_input(
        "Tavily API Key",
        type="password",
        placeholder="Enter key or use .env",
        help="Required for real-time localized news search"
    )
    
    # Priority: manual UI input -> .env file
    mistral_api_key = input_mistral or os.getenv("MISTRAL_API_KEY")
    openweather_api_key = input_weather or os.getenv("OPENWEATHER_API_KEY")
    tavily_api_key = input_tavily or os.getenv("TAVILY_API_KEY")

    st.divider()
    st.markdown("**Tool & Model Status:**")
    st.write(f"• **Reasoning Engine (Mistral):** {'🟢 Active' if mistral_api_key else '🔴 Not Found'}")
    st.write(f"• **Telemetry Tool (OpenWeather):** {'🟢 Active' if openweather_api_key else '🔴 Not Found'}")
    st.write(f"• **News Retrieval Tool (Tavily):** {'🟢 Active' if tavily_api_key else '🔴 Not Found'}")
    
    st.divider()
    require_approval = st.toggle("Human-in-the-Loop (HITL) Guardrail", value=True, help="Pause execution and require manual confirmation before running external tools.")
    
    if st.button("🗑️ Reset Chat & Memory", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_tool_call = None
        st.rerun()

# =========================================================
# 🛠️ Tools Definition
# =========================================================
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    if not openweather_api_key:
        return "Error: Missing OpenWeather API Key."
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={openweather_api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if str(data.get("cod")) != "200":
            return f"Error: {data.get('message', 'Could not fetch weather')}"
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Weather in {city}: {desc}, {temp}°C"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""
    if not tavily_api_key:
        return "Error: Missing Tavily API Key."
        
    try:
        client = TavilyClient(api_key=tavily_api_key)
        response = client.search(
            query=f"latest news in {city}",
            search_depth="basic",
            max_results=3
        )
        results = response.get("results", [])
        if not results:
            return f"No news found for {city}"
        
        news_list = []
        for r in results:
            title = r.get("title", "No title")
            url = r.get("url", "")
            snippet = r.get("content", "")
            news_list.append(f"- **{title}**\n  🔗 [{url}]({url})\n  📝 {snippet[:120]}...")
        
        return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)
    except Exception as e:
        return f"Error fetching news: {str(e)}"

TOOLS = {"get_weather": get_weather, "get_news": get_news}

# =========================================================
# 💬 Session State Management
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_tool_call" not in st.session_state:
    st.session_state.pending_tool_call = None

# =========================================================
# 🖥️ Chat UI Header & History Rendering
# =========================================================
st.title("🌆 AetherCity")
st.caption("A Human-in-the-Loop Conversational Agent for Real-Time City Telemetry, Local News, and General Inquiries.")

for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    if isinstance(msg, (HumanMessage, AIMessage)) and msg.content:
        with st.chat_message(role):
            st.markdown(msg.content)

# =========================================================
# ⏸️ Human-in-the-Loop Pending Approval Section
# =========================================================
if st.session_state.pending_tool_call:
    pending = st.session_state.pending_tool_call
    tool_name = pending["tool_name"]
    tool_args = pending["tool_args"]
    
    with st.chat_message("assistant"):
        st.warning(f"🛡️ **HITL Guardrail Triggered:** The agent requests permission to execute `{tool_name}` with parameters: `{tool_args}`.")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("✅ Authorize Tool Execution", use_container_width=True, type="primary"):
                with st.spinner(f"Executing tool `{tool_name}`..."):
                    tool_fn = TOOLS[tool_name]
                    tool_output = tool_fn.invoke(tool_args)
                    
                    tool_msg = ToolMessage(
                        content=str(tool_output),
                        tool_call_id=pending["tool_call_id"]
                    )
                    st.session_state.messages.append(tool_msg)
                    
                    llm = ChatMistralAI(model="mistral-small-2506", mistral_api_key=mistral_api_key)
                    final_response = llm.bind_tools(list(TOOLS.values())).invoke(st.session_state.messages)
                    
                    st.session_state.messages.append(final_response)
                    st.session_state.pending_tool_call = None
                    st.rerun()

        with col2:
            if st.button("❌ Deny & Continue", use_container_width=True):
                tool_msg = ToolMessage(
                    content="Tool call denied by user.",
                    tool_call_id=pending["tool_call_id"]
                )
                st.session_state.messages.append(tool_msg)
                
                llm = ChatMistralAI(model="mistral-small-2506", mistral_api_key=mistral_api_key)
                final_response = llm.bind_tools(list(TOOLS.values())).invoke(st.session_state.messages)
                
                st.session_state.messages.append(final_response)
                st.session_state.pending_tool_call = None
                st.rerun()

# =========================================================
# 🚀 User Input & Agent Orchestration
# =========================================================
user_prompt = st.chat_input("Ask a general question or inquire about city weather and news...")

if user_prompt and not st.session_state.pending_tool_call:
    if not mistral_api_key:
        st.error("Mistral API Key is missing. Please configure it in `.env` or in the sidebar.")
    else:
        user_msg = HumanMessage(content=user_prompt)
        st.session_state.messages.append(user_msg)
        
        with st.chat_message("user"):
            st.markdown(user_prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("AetherCity reasoning in progress..."):
                llm = ChatMistralAI(model="mistral-small-2506", mistral_api_key=mistral_api_key)
                llm_with_tools = llm.bind_tools(list(TOOLS.values()))
                
                response = llm_with_tools.invoke(st.session_state.messages)
                
                if response.tool_calls:
                    st.session_state.messages.append(response)
                    first_call = response.tool_calls[0]
                    
                    if require_approval:
                        st.session_state.pending_tool_call = {
                            "tool_name": first_call["name"],
                            "tool_args": first_call["args"],
                            "tool_call_id": first_call["id"]
                        }
                        st.rerun()
                    else:
                        tool_fn = TOOLS[first_call["name"]]
                        tool_output = tool_fn.invoke(first_call["args"])
                        tool_msg = ToolMessage(content=str(tool_output), tool_call_id=first_call["id"])
                        st.session_state.messages.append(tool_msg)
                        
                        final_res = llm_with_tools.invoke(st.session_state.messages)
                        st.session_state.messages.append(final_res)
                        st.markdown(final_res.content)
                else:
                    st.session_state.messages.append(response)
                    st.markdown(response.content)