from functools import lru_cache

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

system_prompt = """
You are an assistant that helps users with questions about Magic: The Gathering rules and cards.
If the question isn't about Magic: The Gathering, explain politely that you can only answer questions about Magic: The Gathering game and give examples of questions you can answer.
Always assume the question is about Magic: The Gathering, even when it is not explicitly mentioned.
Give the best answer you can using tools to retrieve relevant informations about rules and cards.
Always format the answer in markdown and in the same language as the question.
Image should be format as ![image](url).
"""  # noqa: E501


@lru_cache
def get_model() -> BaseChatModel:
    # Mistral Nemo from Scaleway
    # return ChatOpenAI(
    #     model="mistral-nemo-instruct-2407",
    #     base_url="https://api.scaleway.ai/v1",
    #     api_key=os.environ["SCW_SECRET_KEY"],  # type: ignore
    # )

    # Deepseek R1 from Scaleway
    # return ChatOpenAI(
    #     model="deepseek-r1-distill-llama-70b",
    #     base_url="https://api.scaleway.ai/v1",
    #     api_key=os.environ["SCW_SECRET_KEY"],  # type: ignore
    # )

    # Llama 3.3 from Scaleway
    # return ChatOpenAI(
    #     model="llama-3.3-70b-instruct",
    #     base_url="https://api.scaleway.ai/v1",
    #     api_key=os.environ["SCW_SECRET_KEY"],  # type: ignore
    # )

    # GPT-4o from OpenAI
    return ChatOpenAI(model="gpt-4o")
