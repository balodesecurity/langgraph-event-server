from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
from agents.llm_model import _default_llm


class StockState(TypedDict):
    stock_name: str
    classification: str  # exchange and sector, populated by _classify
    research_notes: str  # real-time findings from Tavily, populated by _research
    analysis: str        # final analyst-style report, populated by _analyze


_search_tool = TavilySearch(max_results=3)
_react_agent = create_react_agent(_default_llm, [_search_tool])


def _classify(state: StockState) -> dict:
    # LLM-only: identifies exchange and sector from training knowledge, no search needed
    result = _default_llm.invoke([
        HumanMessage(content=(
            f"Identify '{state['stock_name']}': what exchange it trades on and what sector/industry it's in. "
            "Be brief, 2-3 sentences."
        ))
    ])
    return {"classification": result.content}


def _research(state: StockState) -> dict:
    # ReAct loop: LLM decides what to search, calls Tavily one or more times,
    # then synthesizes raw search results into concise research notes
    result = _react_agent.invoke({
        "messages": [HumanMessage(content=(
            f"Research {state['stock_name']} ({state['classification']}). "
            "Use search to find recent news, financial performance, and notable developments. "
            "Summarize your key findings concisely."
        ))]
    })
    return {"research_notes": result["messages"][-1].content}


def _analyze(state: StockState) -> dict:
    # LLM-only: synthesizes classification + research notes into a structured
    # analyst report covering business overview, recent developments, and risks
    result = _default_llm.invoke([
        HumanMessage(content=(
            f"Based on the following about {state['stock_name']}, write a concise analyst-style summary:\n\n"
            f"Profile: {state['classification']}\n\n"
            f"Research: {state['research_notes']}\n\n"
            "Structure: 1) Business overview  2) Recent developments  3) Key risk factors. "
            "Keep it to 3-4 short paragraphs."
        ))
    ])
    return {"analysis": result.content}


def build_stock_graph():
    # Wires the three nodes in sequence: classify -> research -> analyze
    graph = StateGraph(StockState)
    graph.add_node("classify", _classify)
    graph.add_node("research", _research)
    graph.add_node("analyze", _analyze)
    graph.set_entry_point("classify")
    graph.add_edge("classify", "research")
    graph.add_edge("research", "analyze")
    graph.add_edge("analyze", END)
    return graph.compile()
