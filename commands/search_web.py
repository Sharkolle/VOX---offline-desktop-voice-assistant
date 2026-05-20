# commands/search_web.py

# This module handles web search functionality for VOX.
# It takes a search query as input, opens the search results in the default web browser,
# and provides spoken confirmation to the user.

import webbrowser

def search_google(query: str) -> dict:
    """
    Opens a Google search for the given query in the default web browser.

    Args:
        query (str): The search terms provided by the user.

    Returns:
        dict: {'text': str, 'speak': str} → for display and spoken confirmation.
    """
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

    return {
        "text": f"Searching Google for: {query}",
        "speak": f"Searching Google for {query}."
    }
