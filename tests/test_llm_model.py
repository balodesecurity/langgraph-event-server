from unittest.mock import MagicMock
from agents.llm_model import LLMAgent, _default_llm


def test_default_llm_is_shared():
    # Both agents should reuse the same client instance
    a1 = LLMAgent("prompt one")
    a2 = LLMAgent("prompt two")
    assert a1.llm is a2.llm


def test_explicit_llm_overrides_default():
    custom_llm = MagicMock()
    agent = LLMAgent("prompt", llm=custom_llm)
    assert agent.llm is custom_llm


def test_invoke_returns_string():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "mocked response"

    agent = LLMAgent("you are helpful", llm=mock_llm)
    result = agent.invoke("hello")
    assert result == "mocked response"
