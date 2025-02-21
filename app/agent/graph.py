from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.conditions.grade_documents import grade_documents
from app.agent.nodes.node_agent import agent
from app.agent.nodes.node_generator import generate
from app.agent.nodes.node_rewriter import rewrite
from app.agent.nodes.node_trim_history import trim_history
from app.agent.state import AgentState
from app.agent.tools.tool_mtg_card import mtg_card_fetcher
from app.agent.tools.tool_mtg_rules import mtg_rules_retriever

# TOOLS
tools = ToolNode([mtg_rules_retriever, mtg_card_fetcher])

workflow = StateGraph(AgentState)

# NODES
workflow.add_node("agent", agent)
workflow.add_node("tools", tools)
workflow.add_node("rewrite", rewrite)
workflow.add_node("generate", generate)
workflow.add_node("trim_history", trim_history)


# EDGES
workflow.add_edge(START, "trim_history")
workflow.add_edge("trim_history", "agent")
workflow.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
workflow.add_conditional_edges("tools", grade_documents)
workflow.add_edge("rewrite", "agent")
workflow.add_edge("generate", END)

# Compile
checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
