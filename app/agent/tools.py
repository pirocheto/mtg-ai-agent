import requests
from langchain_core.tools import tool

from app.agent.config import vector_store
from app.agent.types import MTGCard


def fetch_from_scryfall(card_name, set_code=None) -> None | MTGCard:
    """Utility function to fetch a card from the Scryfall API."""

    params = {"fuzzy": card_name, "set_code": set_code, "format": "json"}

    response = requests.get(
        "https://api.scryfall.com/cards/named",
        params=params,
        timeout=5,
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    card: dict = response.json()

    return MTGCard(
        name=card["name"],
        lang=card["lang"],
        mana_cost=card["mana_cost"],
        cmc=card["cmc"],
        type_line=card["type_line"],
        oracle_text=card["oracle_text"],
        colors=card["colors"],
        color_identity=card["color_identity"],
        released_at=card["released_at"],
        keywords=card["keywords"],
        reserved=card["reserved"],
        game_changer=card["game_changer"],
        power=card.get("power"),
        image_uri=card.get("image_uris", {}).get("normal"),
        toughness=card.get("toughness"),
        loyalty=card.get("loyalty"),
        legalities=card["legalities"],
    )


@tool
def mtg_card_fetcher(card_name: str, set_code=None) -> MTGCard | None:
    """
    Use this to look up informations about a MTG card to better assist user with their questions.

    Information return by this tool are:
    - name
    - lang
    - mana_cost
    - cmc
    - type_line
    - oracle_text
    - colors
    - color_identity
    - released_at
    - keywords
    - reserved
    - game_changer
    - image_uri
    - power
    - toughness
    - loyalty
    - legalities

    Args:
        card_name (str): The name of the card to look up.
        set_code (str): The set code of the card to look up.

    Returns:
        MTGCard | None: The MTG card information or None if the card is not found
    """

    return fetch_from_scryfall(card_name, set_code)


@tool
def mtg_rules_retriever(query: str) -> list[tuple[str, str]]:
    """
    Use this to look up MTG rules to better assist user with their questions.
    The query must always be in English.

    Args:
        query (str): The query to search in English.

    Returns:
        list[tuple[str, str]]: A list of tuples containing the rule number and
        the content of the rule.
    """

    retrieved_docs = vector_store.similarity_search(query, k=5)
    retrieved_rules = [
        (doc.metadata["mtg_rule_number"], doc.page_content) for doc in retrieved_docs
    ]
    return retrieved_rules
