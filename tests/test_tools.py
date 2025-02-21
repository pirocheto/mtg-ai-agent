from pprint import pprint

from app.tools.tool_mtg_card import mtg_card_fetcher
from app.tools.tool_mtg_rules import mtg_rules_retriever

rules = mtg_rules_retriever.invoke("What happens when I cast a spell?")

# pprint(rules)

card = mtg_card_fetcher.invoke("Lightnng Bolt")
pprint(card)
