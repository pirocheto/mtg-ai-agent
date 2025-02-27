from functools import lru_cache

from langchain_core.language_models import BaseChatModel


@lru_cache
def get_model() -> BaseChatModel:
    from langchain.chat_models import init_chat_model

    return init_chat_model(
        "openai:gpt-4o",
        # Deepseek is unstable for function calling
        # See https://api-docs.deepseek.com/guides/function_calling
        # "deepseek:deepseek-reasoner",
        # "deepseek:deepseek-chat",
    )

    # Config for model from Scaleway
    # from langchain_openai import ChatOpenAI
    # return ChatOpenAI(
    #     model="mistral-nemo-instruct-2407",
    #     base_url="https://api.scaleway.ai/v1",
    #     api_key=os.environ["SCW_SECRET_KEY"],
    # )


model = get_model()
