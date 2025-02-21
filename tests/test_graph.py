from langchain.schema.runnable.config import RunnableConfig

from app.agent.graph import graph


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


def test_graph():
    question = "Quels sont les types de cartes dans Magic: The Gathering ?"
    inputs = {"messages": [("user", question)]}

    config = RunnableConfig(
        configurable={"thread_id": 1},
    )

    print_stream(graph.stream(inputs, stream_mode="values", config=config))


test_graph()
