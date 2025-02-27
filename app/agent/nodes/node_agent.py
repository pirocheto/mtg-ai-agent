from langchain_core.messages import SystemMessage

from app.agent.config import get_model, system_prompt
from app.agent.state import AgentState
from app.agent.tools.tool_mtg_card import mtg_card_fetcher
from app.agent.tools.tool_mtg_rules import mtg_rules_retriever

model = get_model()
tools = [mtg_rules_retriever, mtg_card_fetcher]
model_with_tools = model.bind_tools(tools)


def agent(state: AgentState):
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply end.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """

    inputs = [SystemMessage(system_prompt)] + state["messages"]  # type: ignore

    response = model_with_tools.invoke(inputs)
    return {"messages": [response]}
