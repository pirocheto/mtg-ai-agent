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
        callbacks=[cl.LangchainCallbackHandler()],
        configurable={"thread_id": cl.context.session.id},
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
