from typing import Optional, TypedDict

import requests
from langchain_core.tools import tool


class Legalities(TypedDict):
    standard: str
    future: str
    historic: str
    timeless: str
    gladiator: str
    pioneer: str
    explorer: str
    modern: str
    legacy: str
    pauper: str
    vintage: str
    penny: str
    commander: str
    oathbreaker: str
    standardbrawl: str
    brawl: str
    alchemy: str
    paupercommander: str
    duel: str
    oldschool: str
    premodern: str
    predh: str


class MTGCard(TypedDict):
    name: str
    lang: str
    mana_cost: str
    released_at: str
    cmc: int
    type_line: str
    colors: list[str]
    color_identity: list[str]
    keywords: list[str]
    reserved: bool
    game_changer: bool
    oracle_text: str
    power: Optional[str]
    image_uri: Optional[str]
    toughness: Optional[str]
    loyalty: Optional[str]
    legalities: Legalities


def _fetch_from_scryfall(card_name, set_code=None) -> None | MTGCard:
    url = "https://api.scryfall.com/cards/named"

    params = {
        "fuzzy": card_name,
        "set_code": set_code,
        "format": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as error:
        print("Error while fetching scryfall:", error)
        return None

    if response.status_code == 404:
        return None

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

    Args:
        card_name (str): The name of the card to look up.
        set_code (str): The set code of the card to look up.

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
    """

    return _fetch_from_scryfall(card_name, set_code)
