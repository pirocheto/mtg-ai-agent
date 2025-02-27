from langchain.prompts import PromptTemplate

from app.agent.config import model
from app.agent.state import AgentState

prompt = """
Look at the input and try to reason about the underlying semantic intent / meaning.
The question may be ambiguous, unclear, or too broad. Try to rephrase it in a more specific way.
The question is always about Magic: The Gathering game.
Here is the initial question:
-------
{question}
-------
Formulate an improved question:
"""

chain_moodel = PromptTemplate.from_template(prompt) | model


def rewrite(state: AgentState):
    """
    Transform the query to produce a better question.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with re-phrased question
    """

    messages = state["messages"]
    question = messages[-1].content

    response = chain_moodel.invoke({"question": question})

    return {"messages": [response]}
