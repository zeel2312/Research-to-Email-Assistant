"""Turns research text into a concise stakeholder‑friendly email."""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from agent.config import GEMINI_API_KEY, MODEL_NAME


class EmailDraftTool:
    """Simple wrapper around an LLM chain so it can be called like a tool."""

    def __init__(self, temperature: float = 0.3):
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            google_api_key=GEMINI_API_KEY,
            temperature=temperature,
        )
        self.chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=(
                    "You are an expert communication assistant. Using the research below, "
                    "compose a clear, engaging email (max 180 words) that summarises the key points "
                    "for a non‑technical stakeholder. <research>{research}</research> Email:"),
                input_variables=["research"],
            ),
        )

    def run(self, research: str) -> str:
        """Blocking call – returns email text.  LC 0.2 may return a dict; handle both."""
        result = self.chain.invoke({"research": research})
        if isinstance(result, str):
            return result.strip()
        # Newer LangChain returns {"text": "…"}
        return str(result.get("text", "")).strip()