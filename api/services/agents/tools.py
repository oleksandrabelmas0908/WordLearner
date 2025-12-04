from langchain_core.tools import tool
import requests


@tool
def search_definition(term: str) -> str:
    """
    Search for definitions of a word from a dictionary API.
    Returns a JSON string containing definitions with quotes and synonyms.
    Use this tool only ONCE per word.
    """

    url = f"https://freedictionaryapi.com/api/v1/entries/en/{term}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error fetching definition for {term}: {response.status_code}")

    data = response.json()

    definitions = []
    for entry in data.get("entries", []):
        
        for sense in entry.get("senses", []):
            one_definition = {
                "definition": sense.get("definition"),
                "quotes": sense.get("quotes", []),
                "synonyms": sense.get("synonyms", []),
            }
            definitions.append(one_definition)

    import json
    return json.dumps(definitions) 