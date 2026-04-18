from agents import config


def test_provider_is_set():
    assert config.LLM_PROVIDER in ("gemini", "claude")


def test_model_is_set():
    assert isinstance(config.LLM_MODEL, str) and len(config.LLM_MODEL) > 0


def test_max_output_tokens_is_positive():
    assert isinstance(config.MAX_OUTPUT_TOKENS, int) and config.MAX_OUTPUT_TOKENS > 0
