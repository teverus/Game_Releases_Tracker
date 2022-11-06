import os
from datetime import datetime
from pathlib import Path

from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import wait_for_key, Key, show_message

COLUMNS = ["Title", "Day", "Month", "Year", "UnixReleaseDate", "Genre", "Hidden"]


class UpdateGames:
    def __init__(self):

        self.db = DataBase(Path("Files/GameReleases.db"))

        print(" Connecting to IGN database...", end="\t")
        self.ign_games = self.get_ign_games()
        print("Done")

        print(" Connecting to own database...", end="\t")
        self.known_games, self.known_index = self.get_known_games(this_month=True)
        print("Done")

        different_length = len(self.ign_games) != len(self.known_games)
        if different_length or len(self.ign_games.compare(self.known_games)):
            self.db.remove_by_index(self.known_index)
            self.db.append_to_table(self.ign_games)
            show_message("Information was updated")

        else:
            show_message("No new games/info on IGN")

        print('\n Press "Enter" to continue...')
        wait_for_key(Key.ENTER)

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
            service=ChromeService(ChromeDriverManager(cache_valid_range=30).install()),
            options=options,
            desired_capabilities=capabilities,
        )

        return driver

    def get_game_cards(self):
        cards_xpath = "//*[contains(@class, 'side-by-side-card')]"
        game_cards = self.driver.find_elements(By.XPATH, cards_xpath)

        games = DataFrame([], columns=COLUMNS)

        for i, game_card in enumerate(game_cards):
            title, genre, release_date = game_card.text.split("\n")
            day, month, year = self.get_release_date(release_date)
            unix_release_date = self.get_unix_release_date(day, month, year)
            hidden = "0"
            games.loc[i] = [title, day, month, year, unix_release_date, genre, hidden]

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

    def get_known_games(self, this_month=False):
        df = self.db.read_table()

        if this_month:
            month = f"{datetime.now():%b}".upper()
            year = f"{datetime.now():%Y}".upper()
            df = df.loc[(df.Month == month) & (df.Year == year)]

        proper_index = list(df.index)
        df = df.reset_index(drop=True)
        return df, proper_index

    @staticmethod
    def get_unix_release_date(day, month, year):
        if day:
            expected_date = f"{day.rjust(2, '0')} {month} {year}"
            date = datetime.strptime(expected_date, "%d %b %Y").timestamp()

            return str(int(date))


if __name__ == "__main__":
    UpdateGames()
