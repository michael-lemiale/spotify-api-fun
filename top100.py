import requests
import re

from datetime import datetime as dt

from bs4 import BeautifulSoup


class Top100Song():
    """Scrape Billboard Top 100 Songs
    
    Functionality
        * Scrape billboard.com, get top 100 songs for a time frame
    
    Attributes
        unallowed_values: html values to ignore from scraping the site
        url: the url we are scraping
        timeframe: YYYY-MM-DD time we want to search for Top 100 songs
        year: truncate timeframe and get YYYY string
    """
    def __init__(self) -> None:
        self.unallowed_values = ["-", "NEW", "RE-ENTRY"]
        self.url = "https://www.billboard.com/charts/hot-100"
        self.timeframe = self._get_user_input()
        self.year = dt.strftime(dt.strptime(self.timeframe, "%Y-%m-%d"), "%Y")


    def get_top_100_songs(self) -> list:
        """Scrape billboard top 100 site page with Beautiful Soup and return list of top 100 songs, artists"""
        soup = self._create_html_soup()
        song_titles = soup.find_all(name="li", 
                                    class_="o-chart-results-list__item")        
        artist_and_song_list = []
        
        for data in song_titles:
            artist_and_song = None
            try:
                artist = data.span.getText()
                artist = re.sub(r"[\n\t]*", "", artist)
                if artist.isnumeric() or artist in self.unallowed_values:
                    pass
                else:
                    artist_and_song = {}
                    artist_and_song["artist"] = artist
            except AttributeError:
                pass

            try:
                song = data.h3.getText()
                song = re.sub(r"[\n\t\s]*", "", song)
                if artist.isnumeric() or artist in self.unallowed_values:
                    pass
                else:
                    artist_and_song["song"] = song        
            except AttributeError:
                pass

            if artist_and_song:
                artist_and_song_list.append(artist_and_song)
        
        return artist_and_song_list

    def _create_html_soup(self) -> BeautifulSoup:
        """Create BeautifulSoup class based on URL provided"""
        response = requests.get(self._define_url())
        return BeautifulSoup(response.text, "html.parser")

    def _define_url(self) -> str:
        """Create url based on user input"""
        return f"{self.url}/{self.timeframe}"

    def _get_user_input(self) -> str:
        """Get user input for timeframe we're searching on the billboard site"""
        user_input = input("Date: ('YYYY-MM-DD') ")
        return user_input
