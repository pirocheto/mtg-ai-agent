from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openai:gpt-4o",
    # "deepseek:deepseek-reasoner",
)
