# Architectural Decisions & Technical Trade-Offs

## 1. Human-in-the-Loop (HITL) Tool Authorization
- **Decision:** Implemented an explicit interception step before executing external API tools (`get_weather`, `get_news`).
- **Rationale:** Autonomous agent execution of external APIs or database queries introduces security and cost risks. Requiring explicit user confirmation ensures control over rate limits, data privacy, and tool hallucination.

## 2. Stateless Tool Invocation with LangChain Core Messages
- **Decision:** Kept tool functions purely stateless and relied on `HumanMessage`, `AIMessage`, and `ToolMessage` abstractions for maintaining history across turns.
- **Rationale:** Separating tool execution from state management simplifies debugging and prevents stale context from corrupting conversational history.

## 3. UI Key Fallback Strategy
- **Decision:** Designed a dual-source credential resolver in the Streamlit sidebar (Manual UI input with `.env` fallback).
- **Rationale:** Allows non-technical stakeholders to test the application immediately using their own API credentials without needing to configure local environment files.

## 4. Middleware Pattern for CLI Execution
- **Decision:** Used a functional wrapper (`wrap_tool_call`) in the CLI loop to intercept and inspect tool names and parameters prior to execution.
- **Rationale:** Provides a clean separation of concerns between LLM agent inference and administrative execution controls.
