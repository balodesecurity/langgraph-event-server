from agents.stock.graph import build_stock_graph

_graph = build_stock_graph()


def handle_stock(payload: dict) -> str:
    stock_name = payload.get("stock_name", "unknown")
    result = _graph.invoke({"stock_name": stock_name})
    return result["analysis"]
