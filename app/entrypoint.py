import sys
from pathlib import Path
from typing import cast

import chainlit as cl
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import BaseMessage, HumanMessage

# Add the parent directory to the sys.path so that the app module
# can be imported with `chainlit run` command
sys.path.append(Path(__file__).parents[1].as_posix())

from app.agent.graph import graph


@cl.on_chat_start
async def start():
    commands = [
        {"id": "show", "icon": "image", "description": "Show card image"},
    ]

    await cl.context.emitter.set_commands(commands)


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Explain card 'Serra Angel'",
            message="Explain what the card 'Serra Angel' does in Magic: The Gathering. "
            "Give me a brief overview of the card and its abilities.",
        ),
        cl.Starter(
            label="Explain 'The stack' rule",
            message="Explain 'The Stack' rule for a beginner with anology.",
        ),
        cl.Starter(
            label="Explain the concept of 'Mana Curve'",
            message="Explain the concept of 'Mana Curve'",
        ),
        cl.Starter(
            label="Card interaction: Tarmogoyf vs Lightning Bolt",
            message="Can I kill a Tarmogoyf with a Lightning Bolt "
            "if all graveyards contain a sorcery, and a land?",
        ),
        cl.Starter(
            label="Show card 'Fatal Push'",
            message="Only show the image of the card 'Fatal Push' "
            "without any explanation.",
        ),
    ]


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


@cl.on_message
async def on_message(msg: cl.Message):
    config = RunnableConfig(
        # callbacks=[cl.LangchainCallbackHandler()],
        configurable={"thread_id": cl.context.session.id},
    )

    if msg.command == "show":
        msg.content = (
            f"Only show the image of the card {msg.content} without any explanation."
        )

    final_answer = cl.Message(content="")
    inputs = {"messages": [HumanMessage(msg.content)]}

    for chunk_msg, metadata in graph.stream(
        inputs,
        stream_mode="messages",
        config=config,
    ):
        chunk_msg = cast(BaseMessage, chunk_msg)
        metadata = cast(dict, metadata)

        if (
            chunk_msg.content
            and type(chunk_msg) is not HumanMessage
            and metadata["langgraph_node"] in ["agent", "generate"]
        ):
            chunk_msg.content = cast(str, chunk_msg.content)
            await final_answer.stream_token(chunk_msg.content)

    await final_answer.send()
