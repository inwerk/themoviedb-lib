import io
import re
import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from functools import cache
from typing import Optional


class Request:
    """ Class providing methods for sending HTTP requests to the website <www.themoviedb.org>. """

    @classmethod
    def get(cls, path: str = "", query: str = "", stream: bool = False) -> requests.Response:
        """
        Sends an HTTP GET request to TMDb and returns the response.

        :param path: URL path.
        :param query: URL query string.
        :param stream: Set this parameter for downloading images.
        :return: Response.
        """

        # build a TMDb URL
        url = f"https://www.themoviedb.org{path}?{query}"

        # headers to send with the request
        headers = {"User-Agent": UserAgent().random}

        # send a GET request using URL and headers
        response = requests.get(url, headers=headers, stream=stream)

        # if the response status code was between 200 and 400, return the response
        if response:
            return response

        # HTTP 404: The requested resource was not found
        if response.status_code == 404:
            raise Exception(f"The resource www.themoviedb.org{path} does not exist.")

        # other HTTP status codes
        raise Exception(f"An error occurred while handling your request to www.themoviedb.org{path}.")

    @classmethod
    def image(cls, file_path: str) -> io.BytesIO:
        """
        Downloads an image from TMDb.

        :param file_path: Path to the image.
        :return: Image as BytesIO.
        """

        response = Request.get(path=file_path, stream=True)

        return io.BytesIO(response.content)


class API:
    """ Class providing methods for sending and processing TMDb API requests. """

    @classmethod
    @cache
    def languages(cls, iso_639: bool = True) -> list:
        """
        Returns a list of languages supported by TMDb.

        :param iso_639: Return ISO-639-1 formatted language codes.
        :return: List of supported languages as IETF language tags.
        """

        # get HTTP response for the TMDb start page
        response = Request.get()

        # parse response to BeautifulSoup object
        html_page = BeautifulSoup(response.text, features="html.parser")

        # extract language codes from HTML page
        languages = []
        for link_rel in html_page.find_all("link", {"rel": "alternate"}):

            # if string is IETF language tag
            if re.fullmatch(r"[a-z]{2}-[A-Z]{2}", link_rel.get("hreflang")):
                language = link_rel.get("hreflang")

                # ISO-639-1 formatted language codes
                if iso_639:
                    # remove territory from IETF language tag (e.g. "-DE" or "-AT"
                    language = re.search(r"[a-z]{2}", language).group()

                    # ignore duplicates (e.g. "de-DE" and "de-AT")
                    if language in languages:
                        continue

                    # "cn" (Cantonese) is not included in the ISO-639-1 standard
                    if language == "cn":
                        continue

                # add language tag to list
                languages.append(language)

        return languages

    @classmethod
    @cache
    def categories(cls) -> list:
        """
        Returns a list of categories supported by TMDb.

        :return: List of supported categories as strings.
        """

        # get HTTP response for the TMDb search page
        response = Request.get(path="/search")

        # parse response to BeautifulSoup object
        html_page = BeautifulSoup(response.text, features="html.parser")

        # extract categories from HTML page
        categories = []
        for a_search_tab in html_page.find_all("a", {"class": "search_tab"}):
            if a_search_tab.get("id") is not None:
                categories.append(a_search_tab.get("id"))

        return categories

    @classmethod
    def poster_path(cls, poster_id: str, original_resolution: bool = True,
                    width: int = None, height: int = None) -> str:
        """
        Returns the TMDb URL path for a poster image. Allowed sizes: 94x141, 188x282, 150x225, 300x450, 600x900.

        :param poster_id: The poster ID.
        :param original_resolution: Whether to return the path for the original resolution of the image.
        :param width: The width of the image.
        :param height: The height of the image.
        :return: Poster path as string.
        """

        if original_resolution and width is None and height is None:
            return f"/t/p/original/{poster_id}.jpg"

        if not any([width == 94 and height == 141, width == 188 and height == 282, width == 150 and height == 225,
                    width == 300 and height == 450, width == 600 and height == 900]):

            raise ValueError("Image size not supported.")

        return f"/t/p/w{width}_and_h{height}_bestv2/{poster_id}.jpg"

    @classmethod
    def __search_results(cls, html_page: BeautifulSoup, language: str) -> list:
        search_results = []
        for div_card in html_page.find_all('div', {'class': 'card v4 tight'}):
            tmdb_entry = TMDbEntry(language=language)

            div_title = div_card.find('div', {'class': 'title'})

            if div_title.find('a') is not None:
                tmdb_entry.category = div_title.find('a').get('data-media-type')

            if div_title.find('a') is not None:
                tmdb_entry.tmdb_id = re.search(r'(\d+)', div_title.find('a').get('href')).group()

            if div_title.find('h2') is not None:
                result.title = div_title.find('h2').next_element.strip().replace('amp;', '')

            if div_title.find('span', {'class': 'release_date'}) is not None:
                tmdb_entry.release_year = re.search(r'(\d){4}', div_title
                                                    .find('span', {'class': 'release_date'}).get_text()).group()

            if div_card.find('p') is not None:
                tmdb_entry.description = div_card.find('p').get_text()

            if div_card.find('img') is not None:
                tmdb_entry.poster_id = (re.search(r'(\w)+.jpg', div_card.find('img').get('src')).group()
                                        .replace(".jpg", ""))

            search_results.append(tmdb_entry)

        return search_results

    @classmethod
    @cache
    def search(cls, query: str = '', page: int = 1, language: str = "en",
               recursive: bool = False, max_pages: int = 10) -> list:
        """
        Search for movies or tv series by their original, translated and alternative titles.
        """

        # build a search request for TMDb
        path = f'/search'
        query = f"language={language}&page={page}&query={query}"

        # get response from TMDb request
        response = Request.get(path=path, query=query)

        # parse response to BeautifulSoup object
        html_page = BeautifulSoup(response.text, features='html.parser')

        # get search results from html page
        search_results = cls.__search_results(html_page, language=language)

        # if recursive is set, call search for every page after the current
        if recursive and max_pages > 1:
            if html_page.find('span', {'class': 'page next'}):
                search_results += cls.search(query=query, page=page + 1, language=language,
                                             recursive=True, max_pages=max_pages - 1)

        return search_results

    class Movie:
        @classmethod
        def details(cls):
            """
            TODO: method to get information for a specific movie
            """

            raise NotImplementedError()

        @classmethod
        def poster_id(cls):
            """
            TODO: method to get the poster_id for a specific movie
            """

            raise NotImplementedError()

    class TV:
        @classmethod
        def details(cls):
            """
            TODO: method to get information for a specific tv series
            """

            raise NotImplementedError()

        @classmethod
        def poster_id(cls):
            """
            TODO: method to get the poster_id for a specific tv series
            """

            raise NotImplementedError()

        @classmethod
        @cache
        def seasons(cls, series_id: str) -> list:
            # build a request for TMDb
            path = f"/tv/{series_id}/seasons"

            # get response from TMDb request
            response = Request.get(path=path)

            # parse response to BeautifulSoup object
            html_page = BeautifulSoup(response.text, features="html.parser")

            # extract seasons from HTML page
            seasons = []
            for season in html_page.find_all("div", {"class": "season_wrapper"}):
                season_number = (re.search(r"season/(\d+)", season.find("h2").find("a").get("href")).group()
                                 .replace("season/", ""))
                seasons.append(season_number)

            return seasons

        @classmethod
        def number_of_seasons(cls, series_id: str) -> int:
            # get seasons for the tv show
            seasons = API.TV.seasons(series_id=series_id)

            # remove season '0'
            if "0" in seasons:
                seasons.remove("0")

            # return season count
            return len(seasons)

        @classmethod
        @cache
        def episodes(cls, series_id: str, season_id: str, language: str = "en") -> list:
            # build a request for TMDb
            path = f"/tv/{series_id}/season/{season_id}"
            query = f"language={language}"

            # get response from TMDb request
            response = Request.get(path=path, query=query)

            # parse response to BeautifulSoup object
            html_page = BeautifulSoup(response.text, features="html.parser")

            # extract episodes from HTML page
            episodes = []
            for div_card in html_page.find_all("div", {"class": "card"}):
                episode_number = div_card.find("span", {'class': "episode_number"}).get_text()
                episode_title = (div_card.find("div", {"class": "episode_title"}).find("a").get_text()
                                 .replace("amp;", ""))
                episodes.append({"number": episode_number, "title": episode_title})

            return episodes


class TMDbEntry:
    def __init__(self, category: str = None, tmdb_id: str = None, title: str = None, release_year: str = None,
                 description: str = None, poster_id: str = None, language: str = "en"):
        self.category = category
        self.tmdb_id = tmdb_id
        self.title = title
        self.release_year = release_year
        self.description = description
        self.poster_id = poster_id
        self.language = language

    def __str__(self):
        if self.title is None:
            return 'Not available'
        if self.release_year is None:
            return f'{self.title}'

        return f'{self.title} ({self.release_year})'

    def __eq__(self, other: "TMDbEntry") -> bool:
        return (self.category == other.category
                and self.tmdb_id == other.tmdb_id)

    @property
    def category(self) -> Optional[str]:
        return self._category

    @category.setter
    def category(self, category: str = None) -> None:
        if category is not None:
            if not isinstance(category, str):
                raise TypeError("TMDbEntry category must be a string.")

            if category not in API.categories():
                raise ValueError("TMDbEntry category must be 'movie' or 'tv'.")

        self._category = category

    @property
    def tmdb_id(self) -> Optional[str]:
        return self._tmdb_id

    @tmdb_id.setter
    def tmdb_id(self, tmdb_id: str = None) -> None:
        if tmdb_id is not None:
            if not isinstance(tmdb_id, str):
                raise TypeError("TMDbEntry tmdb_id must be a string.")

            if not tmdb_id.isnumeric():
                raise ValueError("TMDbEntry tmdb_id must be numeric.")

            if tmdb_id == "0":
                raise ValueError("TMDbEntry tmdb_id must be greater than 0.")

        self._tmdb_id = tmdb_id

    @property
    def title(self) -> Optional[str]:
        return self._title

    @title.setter
    def title(self, title: str = None) -> None:
        if title is not None:
            if not isinstance(title, str):
                raise TypeError("TMDbEntry title must be a string.")

        self._title = title

    @property
    def release_year(self) -> Optional[str]:
        return self._release_year

    @release_year.setter
    def release_year(self, release_year: str = None) -> None:
        if release_year is not None:
            if not isinstance(release_year, str):
                raise TypeError("TMDbEntry release_year must be a string.")

            if not release_year.isnumeric():
                raise ValueError("TMDbEntry release_year must be numeric.")

        self._release_year = release_year

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, description: str = None) -> None:
        if description is not None:
            if not isinstance(description, str):
                raise TypeError("TMDbEntry description must be a string.")

        self._description = description

    @property
    def poster_id(self) -> Optional[str]:
        return self._poster_id

    @poster_id.setter
    def poster_id(self, poster_id: str = None) -> None:
        if poster_id is not None:
            if not isinstance(poster_id, str):
                raise TypeError("TMDbEntry poster_id must be a string.")

        self._poster_id = poster_id

    @property
    def language(self) -> Optional[str]:
        return self._language

    @language.setter
    def language(self, language: str = None) -> None:
        if language is not None:
            if not isinstance(language, str):
                raise TypeError("TMDbEntry language must be a string.")

            if language not in API.languages():
                raise ValueError(f"TMDbEntry language must be one of the following: {API.languages()}.")

        self._language = language

    def format_plex(self) -> str:
        """
        Formats a file name according to the Plex scheme.\n
        https://support.plex.tv/articles/naming-and-organizing-your-movie-media-files/\n
        https://support.plex.tv/articles/naming-and-organizing-your-tv-show-files/\n

        :return: File name in Plex formatting.
        """

        if self.tmdb_id is None:
            return f'{self}'

        return f'{self} {{tmdb-{self.tmdb_id}}}'

    def is_movie(self) -> bool:
        """
        Returns whether the entry is a movie.

        :return: Is (not) a movie.
        """
        if self.category is None:
            return False

        return self.category == "movie"

    def is_tv(self) -> bool:
        """
        Returns whether the entry is a TV show.

        :return: Is (not) a TV show.
        """
        if self.category is None:
            return False

        return self.category == "tv"

    def poster(self, resolution: str = "original", high_resolution: bool = False) -> Optional[io.BytesIO]:
        """
        Returns the poster of this TMDbEntry. By default, with a resolution of 94x141.

        :param resolution: Specify the desired resolution for the image (e.g. 'original', 'low', 'medium' or 'high').
        :parameter high_resolution: Specify whether the image should be returned in a higher resolution (600x900).
        :return: Poster image.
        """

        if self.poster_id is None:
            return None

        if high_resolution:
            resolution = "high"

        match resolution:
            case "original":
                return Request.image(file_path=API.poster_path(poster_id=self.poster_id, original_resolution=True))
            case "low":
                return Request.image(file_path=API.poster_path(poster_id=self.poster_id, width=150, height=225))
            case "medium":
                return Request.image(file_path=API.poster_path(poster_id=self.poster_id, width=300, height=450))
            case "high":
                return Request.image(file_path=API.poster_path(poster_id=self.poster_id, width=600, height=900))
            case _:
                raise ValueError("Specified resolution must be 'low', 'medium', 'high' or 'original'.")

    def seasons(self) -> list:
        """
        Returns a list of all seasons for a TV series.

        :return: List of seasons.
        """

        # raise exception if TMDbEntry is not a TV series
        if not self.is_tv():
            raise Exception(f"TMDbEntry is not a TV series. Category: {self.category}")

        return API.TV.seasons(series_id=self.tmdb_id)

    def episodes(self, season_id: str) -> dict:
        """
        Returns a dictionary mapping all the episodes for a specific season.

        :param season_id: The season id.
        :return: Dictionary mapping the season´s episodes.
        """

        # raise exception if TMDbEntry is not a TV series
        if not self.is_tv():
            raise Exception(f"TMDbEntry is not a TV series. Category: {self.category}")

        return API.TV.episodes(series_id=self.tmdb_id, season_id=season_id, language=self.language)
