from langchain_core.messages import SystemMessage

from app.agent.config import model
from app.agent.state import AgentState
from app.agent.tools.tool_mtg_card import mtg_card_fetcher
from app.agent.tools.tool_mtg_rules import mtg_rules_retriever

tools = [mtg_rules_retriever, mtg_card_fetcher]
model_with_tools = model.bind_tools(tools)


guardrails = """
If the question isn't about Magic: The Gathering, explain politely that you can only answer questions about Magic: The Gathering and give examples of questions you can answer.
Always assume the question is about Magic: The Gathering, even when it is not explicitly mentioned.
Use only the information you have in the context and do not provide any additional information.
If you don't know the answer, just say that you don't know.
"""

system_prompt = f"""
You are an assistant that helps users with questions about Magic: The Gathering rules.
{guardrails}
Give the best answer you can.
Use tools to retrieve relevant informations about rules.
Always display the rule numbers of your information at the end of the response.
Only refer to the rules you have been provided with.
Always format the answer in markdown.
"""


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
