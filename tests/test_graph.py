from pathlib import Path

from dotenv import load_dotenv
from langchain.schema.runnable.config import RunnableConfig

load_dotenv(Path(__file__).parents[1] / "app/.env")

from app.agent.graph import graph


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


def test_graph():
    question = "Que dis la règle Flying ?"
    inputs = {"messages": [("user", question)]}

    config = RunnableConfig(
        configurable={"thread_id": 1},
    )

    print_stream(graph.stream(inputs, stream_mode="values", config=config))


test_graph()
