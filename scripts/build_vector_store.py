import json
import re
from pathlib import Path

import tiktoken
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

load_dotenv()


root_dir = Path(__file__).resolve().parents[1]
data_dir = root_dir / "data"

data_path = data_dir / "MagicCompRules_2020250207.txt"
chunks_path = data_dir / "MagicCompRules_2020250207.chunks.json"
vectorstore_path = data_dir / "MagicCompRules_2020250207.vectorstore"


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count tokens in text."""

    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def create_chunks(data: str, save: bool = False) -> list[Document]:
    """Split documents into chunks."""

    splitted_documents = []
    total_tokens = 0

    pattern = re.compile(r"^\d{3}\.?\d+[a-z]*\.?(?=\s)")

    for chunk in data.split("\n\n"):
        num_tokens = count_tokens(chunk)
        match_rule = pattern.search(chunk)
        doc = Document(
            page_content=chunk.strip(),
            metadata={
                "mtg_rule_number": match_rule.group() if match_rule else "none",
            },
        )
        splitted_documents.append(doc)
        total_tokens += num_tokens

    print(f"Total tokens: {total_tokens}")

    price_per_token = 0.13 / 1_000_000  # $0.13 / 1 M tokens
    print(f"Price for text-embedding-3-large: ${total_tokens * price_per_token:.2f}")

    if save:
        chunks = [doc.model_dump() for doc in splitted_documents]
        chunks_path.write_text(json.dumps(chunks, indent=4))

    return splitted_documents


def create_vector_store(documents: list[Document], save: bool = False) -> FAISS:
    """Create vector database from documents."""

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = FAISS.from_documents(documents, embeddings)

    if save:
        vector_store.save_local(str(vectorstore_path))

    return vector_store


if __name__ == "__main__":
    data = data_path.read_text()
    splitted_documents = create_chunks(data, save=True)
    create_vector_store(splitted_documents, save=True)
