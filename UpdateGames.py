import os

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from Code.functions.db import read_table, write_to_table

COLUMNS = ["Title", "Day", "Month", "Year", "Genre"]
TABLE = "GameReleases"


class UpdateGames:
    def __init__(self):

        print("Checking games on IGN", end="\t")
        self.ign_games = self.get_ign_games()
        print("Done")

        print("Checking games in DB", end="\t")
        self.known_games = self.get_known_games()
        print("Done")

        different_length = len(self.ign_games) != len(self.known_games)
        if different_length or len(self.ign_games.compare(self.known_games)):
            print("Updating known games", end="\t")
            write_to_table(self.ign_games, TABLE)
            print("Done")

        else:
            print("No new games/info on IGN")

    @staticmethod
    def get_driver(headless=False):
        os.environ["WDM_LOG"] = "0"
        os.environ["WDM_LOCAL"] = "1"

        capabilities = DesiredCapabilities().CHROME
        capabilities["pageLoadStrategy"] = "eager"  # "normal"

        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")

        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
            desired_capabilities=capabilities,
        )

        return driver

    def get_game_cards(self):
        cards_xpath = "//*[contains(@class, 'side-by-side-card')]"
        game_cards = self.driver.find_elements(By.XPATH, cards_xpath)

        games = DataFrame([], columns=COLUMNS)

        for index, game_card in enumerate(game_cards):
            title, genre, release_date = game_card.text.split("\n")
            day, month, year = self.get_release_date(release_date)
            games.loc[index] = [title, day, month, year, genre]

        return games

    @staticmethod
    def get_release_date(release_date):
        day = None

        try:
            month, day, year = release_date.replace(",", "").split(" ")
        except ValueError:
            month, year = release_date.split("/")

        return day, month, year

    def get_ign_games(self):
        with self.get_driver(headless=True) as self.driver:
            self.driver.get("https://www.ign.com/upcoming/games/pc")
            game_cards = self.get_game_cards()

            return game_cards

    @staticmethod
    def get_known_games():
        df = read_table(TABLE)

        return df


if __name__ == "__main__":
    UpdateGames()
