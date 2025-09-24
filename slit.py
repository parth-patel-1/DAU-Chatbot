from __future__ import annotations
from typing import Literal, TypedDict
import asyncio, os, json
import streamlit as st
# from dotenv import load_dotenv
from openai import AsyncOpenAI
from supabase import create_client, Client

from pydantic_ai_expert import pydantic_ai_expert, DAU
from pydantic_ai.messages import (
    ModelMessage, ModelRequest, ModelResponse,
    SystemPromptPart, UserPromptPart, TextPart,
    ToolCallPart, ToolReturnPart, RetryPromptPart,
    ModelMessagesTypeAdapter
)

def get_secret(key: str) -> str:
    try:
        return st.secrets[key]  # Streamlit secrets if available
    except Exception:
        return os.getenv(key, "")

OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_SERVICE_KEY = get_secret("SUPABASE_SERVICE_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not set"); st.stop()
if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    st.error("SUPABASE_URL / SUPABASE_SERVICE_KEY not set"); st.stop()
if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    st.error("SUPABASE_URL / SUPABASE_SERVICE_KEY not set"); st.stop()

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

class ChatMessage(TypedDict):
    role: Literal['user', 'model']
    timestamp: str
    content: str

def display_message_part(part):
    # tolerant access (object or dict)
    kind = getattr(part, "part_kind", None) or (part.get("part_kind") if isinstance(part, dict) else None)
    content = getattr(part, "content", None) or (part.get("content") if isinstance(part, dict) else None)
    if not kind:
        return
    if kind == 'system-prompt':
        with st.chat_message("assistant"):
            st.markdown(f"**System**: {content or ''}")
    elif kind == 'user-prompt':
        with st.chat_message("user"):
            st.markdown(content or "")
    elif kind == 'text':
        with st.chat_message("assistant"):
            st.markdown(content or "")

with st.sidebar:
    st.markdown("### 🧩 Info")
    st.markdown("**This is Agentic RAG Chatbot for DAU's website.**")
    st.caption("For more details visit dau.ac.in")
    # st.caption(")
    # show_search_anim = st.toggle("Show cloud cosine-similarity animation", value=True)
    st.divider()
    # st.markdown("#### 👤 Author")
    st.markdown("**Made by: Parth Patel - M.Tech(ML)**")
    st.caption("Email: 202411047@dau.ac.in")
    st.caption("This project is intended solely for learning and is not associated with any official website.")
    if st.button("🗑️ Clear chat"):
        st.session_state["messages"] = []
        st.rerun()



async def run_agent_with_streaming(user_input: str):

    deps = DAU(supabase=supabase, openai_client=openai_client)
    history = st.session_state["messages"][:-1]  # always exists and is a list now

    async with pydantic_ai_expert.run_stream(
        user_input, deps=deps, message_history=history
    ) as result:
        partial_text = ""
        message_placeholder = st.empty()
        async for chunk in result.stream_text(delta=True):
            partial_text += chunk
            message_placeholder.markdown(partial_text)

        # Option A: store only your final rendered text
        st.session_state["messages"].append(
            ModelResponse(parts=[TextPart(content=partial_text)])
        )
async def main():
    st.title("DAU AI Agentic Chatbot")
    st.write("Ask any question about DAU (Dhirubhai Ambani University)")

    if "messages" not in st.session_state or not isinstance(st.session_state.get("messages"), list):
        st.session_state["messages"] = []

    for msg in st.session_state["messages"]:
        if isinstance(msg, (ModelRequest, ModelResponse)):
            for part in getattr(msg, "parts", []):
                display_message_part(part)

    user_input = st.chat_input("What questions do you have about Dhirubhai Ambani University")
    if user_input:
        st.session_state["messages"].append(
            ModelRequest(parts=[UserPromptPart(content=user_input)])
        )
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            await run_agent_with_streaming(user_input)

if __name__ == "__main__":
    asyncio.run(main())
