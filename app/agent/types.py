from typing import Optional, TypedDict


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
