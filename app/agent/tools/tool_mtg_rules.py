from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings

root_dir = Path(__file__).parents[3]
vector_store_path = root_dir / "data/MagicCompRules_2020250207.vectorstore"

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = FAISS.load_local(
    str(vector_store_path),
    embeddings,
    allow_dangerous_deserialization=True,
)


@tool
def mtg_rules_retriever(query: str) -> list[tuple[str, str]]:
    """
    Use this to look up MTG rules to better assist user with their questions.
    The query must always be in English.
    """

    retrieved_docs = vector_store.similarity_search(query, k=5)
    retrieved_rules = [
        (doc.metadata["mtg_rule_number"], doc.page_content) for doc in retrieved_docs
    ]
    # retrieved_rules = [doc.page_content for doc in retrieved_docs]

    return retrieved_rules
