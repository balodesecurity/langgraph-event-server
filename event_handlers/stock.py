from agents import LLMAgent

_agent = LLMAgent(
    system_prompt=(
        "You are a concise stock analyst. "
        "Given a stock name, provide a brief one-paragraph overview of the company "
        "and any notable recent context you know about it. "
        "Do not make up prices or specific financial figures."
    )
)


def handle_stock(payload: dict) -> str:
    stock_name = payload.get("stock_name", "unknown")
    return _agent.invoke(f"Give me a brief overview of: {stock_name}")
