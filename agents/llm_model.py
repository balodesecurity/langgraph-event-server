from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from agents import config


def _build_llm() -> BaseChatModel:
    if config.LLM_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=config.LLM_MODEL, max_output_tokens=config.MAX_OUTPUT_TOKENS)
    if config.LLM_PROVIDER == "claude":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=config.LLM_MODEL, max_tokens=config.MAX_OUTPUT_TOKENS)
    raise ValueError(f"Unknown LLM_PROVIDER: {config.LLM_PROVIDER!r}")


_default_llm: BaseChatModel = _build_llm()


class LLMAgent:
    """Provider-agnostic LLM agent. Driven by agents/config.py; pass an explicit
    llm to override for a specific handler."""

    def __init__(self, system_prompt: str, llm: BaseChatModel | None = None):
        self.system_prompt = system_prompt
        self.llm = llm if llm is not None else _default_llm

    def invoke(self, user_message: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_message),
        ]
        return self.llm.invoke(messages).content
