import webbrowser
from urllib.parse import quote

from bs4 import BeautifulSoup
from requests import get


class OpenInSteam:
    def __init__(self, game_title):
        game_title = game_title.strip().split(" | ")[-1]
        game_title = quote(game_title)

        response = get(url=f"https://www.google.com/search?q={game_title} Steam")
        response.raise_for_status()

        steam_link = None
        for link in BeautifulSoup(response.text, "html.parser").find_all("a"):
            if "https://store.steampowered.com/app/" in link.attrs["href"]:
                steam_link = link.attrs["href"].split("q=")[-1].split("&sa=")[0]
                break

        try:
            webbrowser.open(steam_link)
        except Exception:
            raise Exception(f"Couldn't open {steam_link}")
