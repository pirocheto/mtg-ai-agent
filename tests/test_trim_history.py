from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    trim_messages,
)

messages = [
    HumanMessage("Hello!"),
    SystemMessage("Hello!"),
    HumanMessage("How are you?"),
    SystemMessage("I'm fine."),
    HumanMessage("What's your name?"),
    SystemMessage("I'm a chatbot."),
    HumanMessage("What's your favorite color?"),
    SystemMessage("I like blue."),
]

kept_messages = trim_messages(
    messages,
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


for message in kept_messages:
    message.pretty_print()
