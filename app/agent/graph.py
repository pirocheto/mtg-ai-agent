from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import (
    BaseMessage,
    RemoveMessage,
    SystemMessage,
    trim_messages,
)
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.config import get_model, system_prompt
from app.agent.tools import mtg_card_fetcher, mtg_rules_retriever

tool_list = [mtg_rules_retriever, mtg_card_fetcher]


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]


def trim_history(state: AgentState) -> dict:
    """
    Trim the chat history to a fixed length.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with trimmed history
    """

    current_messages = state["messages"]

    kept_messages = trim_messages(
        current_messages,
        # Keep the last <= n_count tokens of the messages.
        strategy="last",
        # Remember to adjust based on your model
        # or else pass a custom token_encoder
        token_counter=len,
        # Remember to adjust based on the desired conversation
        # length
        max_tokens=10,
        # Most chat models expect that chat history starts with either:
        # (1) a HumanMessage or
        # (2) a SystemMessage followed by a HumanMessage
        start_on="human",
        # Most chat models expect that chat history ends with either:
        # (1) a HumanMessage or
        # (2) a ToolMessage
        # end_on=("human", "tool"),
        end_on="ai",
        # Usually, we want to keep the SystemMessage
        # if it's present in the original history.
        # The SystemMessage has special instructions for the model.
        include_system=False,
    )

    messages_to_delete = [
        RemoveMessage(id=str(m.id)) for m in current_messages if m not in kept_messages
    ]

    return {"messages": messages_to_delete}


def agent(state: AgentState) -> dict:
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, it will decide to use the tools to retrieve relevant informations
    about rules and cards.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """

    model = get_model()
    model_with_tools = model.bind_tools(tool_list)

    inputs = [SystemMessage(system_prompt)] + state["messages"]  # type: ignore

    response = model_with_tools.invoke(inputs)
    return {"messages": [response]}


def create_graph() -> CompiledStateGraph:
    """
    Create the state graph for the agent.
    """

    workflow = StateGraph(AgentState)

    tools = ToolNode(tool_list)

    workflow.add_node("agent", agent)
    workflow.add_node("tools", tools)
    workflow.add_node("trim_history", trim_history)

    workflow.add_edge(START, "agent")
    workflow.add_edge("tools", "agent")
    workflow.add_edge("trim_history", END)
    workflow.add_conditional_edges(
        "agent", tools_condition, {"tools": "tools", END: "trim_history"}
    )

    return workflow.compile()
