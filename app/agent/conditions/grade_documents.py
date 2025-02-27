from typing import Literal, cast

from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from app.agent.config import model
from app.agent.state import AgentState


class Grade(BaseModel):
    """Binary score for relevance check."""

    binary_score: str = Field(description="Relevance score 'yes' or 'no'")


llm = model.with_structured_output(Grade)


template = """You are a grader assessing relevance of a retrieved document to a user question.
Here is the retrieved document: {context}
Here is the user question: {question}
If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant.
Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""


prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"],
)

chain = prompt | llm


def grade_documents(state: AgentState) -> Literal["generate", "rewrite"]:
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (messages): The current state

    Returns:
        str: A decision for whether the documents are relevant or not
    """

    messages = state["messages"]
    last_message = messages[-1]
    first_message = messages[0]

    question = first_message.content
    docs = last_message.content

    scored_result = chain.invoke({"question": question, "context": docs})
    scored_result = cast(Grade, scored_result)
    score = scored_result.binary_score

    if score == "yes":
        return "generate"

    else:
        return "rewrite"
