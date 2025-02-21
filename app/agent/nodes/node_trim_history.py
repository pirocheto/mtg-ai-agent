from langchain.chat_models import init_chat_model
from langchain_core.messages import RemoveMessage, trim_messages

from app.agent.state import AgentState

model = init_chat_model("openai:gpt-4o")


def trim_history(state: AgentState):
    """
    Trim the chat history to a fixed length.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with trimmed history
    """

    current_messages = state["messages"]

    kept_messages = trim_messages(
        current_messages,
        # Keep the last <= n_count tokens of the messages.
        strategy="last",
        # Remember to adjust based on your model
        # or else pass a custom token_encoder
        token_counter=len,
        # Remember to adjust based on the desired conversation
        # length
        max_tokens=10,
        # Most chat models expect that chat history starts with either:
        # (1) a HumanMessage or
        # (2) a SystemMessage followed by a HumanMessage
        start_on="human",
        # Most chat models expect that chat history ends with either:
        # (1) a HumanMessage or
        # (2) a ToolMessage
        end_on=("human", "tool"),
        # Usually, we want to keep the SystemMessage
        # if it's present in the original history.
        # The SystemMessage has special instructions for the model.
        include_system=False,
    )

    delete_messages = [
        RemoveMessage(id=str(m.id)) for m in state["messages"] if m not in kept_messages
    ]
    return {"messages": delete_messages}
