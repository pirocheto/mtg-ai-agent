from langchain_core.messages import SystemMessage

from app.agent.config import model
from app.agent.state import AgentState

system_prompt = """
You are an assistant that helps users with questions about Magic: The Gathering rules.
If you don't know the answer, just say that you don't know.
Give the best answer you can.
Always display the rule numbers of your information at the end of the response.
Only refer to the rules you have been provided with.
Always format the answer in markdown.
"""


def generate(state: AgentState):
    """
    Generate answer

    Args:
        state (messages): The current state

    Returns:
         dict: The updated state with re-phrased question
    """

    inputs = [SystemMessage(system_prompt)] + state["messages"]  # type: ignore

    response = model.invoke(inputs)
    return {"messages": [response]}
