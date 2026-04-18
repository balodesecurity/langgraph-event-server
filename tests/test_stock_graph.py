from unittest.mock import MagicMock
from agents.stock.graph import build_stock_graph, _classify, _research, _analyze


def test_graph_builds():
    graph = build_stock_graph()
    assert graph is not None


def test_graph_has_expected_nodes():
    graph = build_stock_graph()
    assert set(graph.get_graph().nodes.keys()) == {"classify", "research", "analyze", "__start__", "__end__"}


def test_classify_returns_classification(mocker):
    # Replace the frozen Pydantic LLM instance with a plain mock
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Trades on NSE. Oil & gas sector."
    mocker.patch("agents.stock.graph._default_llm", mock_llm)

    result = _classify({"stock_name": "Aegis Logistics", "classification": "", "research_notes": "", "analysis": ""})
    assert result == {"classification": "Trades on NSE. Oil & gas sector."}


def test_analyze_returns_analysis(mocker):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Final analyst report."
    mocker.patch("agents.stock.graph._default_llm", mock_llm)

    state = {
        "stock_name": "Aegis Logistics",
        "classification": "Oil & gas, NSE",
        "research_notes": "45% profit growth",
        "analysis": "",
    }
    result = _analyze(state)
    assert result == {"analysis": "Final analyst report."}


def test_full_graph_invocation(mocker):
    # Mock both LLM and ReAct agent to avoid real API calls
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "mocked"
    mocker.patch("agents.stock.graph._default_llm", mock_llm)

    mock_agent_response = {"messages": [MagicMock(content="mocked research")]}
    mocker.patch("agents.stock.graph._react_agent.invoke", return_value=mock_agent_response)

    graph = build_stock_graph()
    result = graph.invoke({"stock_name": "NVIDIA"})
    assert "analysis" in result
    assert isinstance(result["analysis"], str)
