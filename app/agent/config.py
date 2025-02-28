from functools import lru_cache
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

system_prompt = """
You are an assistant that helps users with questions about Magic: The Gathering rules and cards.
If the question isn't about Magic: The Gathering, explain politely that you can only answer questions about Magic: The Gathering game and give examples of questions you can answer.
Always assume the question is about Magic: The Gathering, even when it is not explicitly mentioned.
Give the best answer you can using tools to retrieve relevant informations about rules and cards.
Always format the answer in markdown and in the same language as the question.
Image should be format as ![image](url).
"""  # noqa: E501


@lru_cache
def get_model() -> BaseChatModel:
    """Get the chat model for the agent."""
    return ChatOpenAI(model="gpt-4o")


@lru_cache
def get_embedding_model() -> Embeddings:
    """Get the embedding model for the agent."""
    return OpenAIEmbeddings(model="text-embedding-3-large")


vector_store_path = (
    Path(__file__).parents[2] / "data/MagicCompRules_2020250207.vectorstore"
)


@lru_cache
def get_vector_store() -> FAISS:
    """Get the vector store for the agent."""
    return FAISS.load_local(
        str(vector_store_path),
        get_embedding_model(),
        allow_dangerous_deserialization=True,
    )
