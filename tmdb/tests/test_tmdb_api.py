import unittest

from .. import *


class TestTMDbAPI(unittest.TestCase):

    # tests for languages()
    def test_languages_iso_639(self):
        """ Check whether language tags match the ISO-639-1 standard."""

        languages = API.languages()

        for language in languages:
            self.assertTrue(re.fullmatch(r"[a-z]{2}", language))

    def test_languages_iso_639_no_duplicates(self):
        """ Check that there are no duplicate language tags."""

        languages = API.languages()

        for language in languages:
            languages.remove(language)
            self.assertFalse(language in languages)

    def test_languages_iso_639_cantonese(self):
        """ Cantonese ("cn") is not included in the ISO-639-1 standard. """

        languages = API.languages()

        self.assertFalse("cn" in languages)

    def test_languages_ietf(self):
        """ Check whether language tags match the IETF standard."""

        languages = API.languages(iso_639=False)

        for language in languages:
            self.assertTrue(re.fullmatch(r"[a-z]{2}-[A-Z]{2}", language))

    def test_languages_ietf_no_duplicates(self):
        """ Check that there are no duplicate language tags."""

        languages = API.languages(iso_639=False)

        for language in languages:
            languages.remove(language)
            self.assertFalse(language in languages)

    # tests for categories()
    def test_categories(self):
        categories = API.categories()
        categories_reference = ['movie', 'tv', 'person', 'collection', 'company', 'keyword', 'network']

        self.assertEqual(categories_reference, categories)

    # tests for search()
    def test_search(self):
        search_results = API.search(query="Star Wars")
        tmdb_entry = TMDbEntry(category="movie", tmdb_id="11")

        self.assertTrue(tmdb_entry in search_results)

    # tests for TV.seasons()
    def test_TV_seasons(self):
        seasons = API.TV.seasons(series_id="253")
        seasons_reference = ['0', '1', '2', '3']

        self.assertEqual(seasons_reference, seasons)

    # tests for TV.episodes()
    def test_TV_episodes(self):
        episodes = API.TV.episodes(series_id="253", season_id="1")
        episodes_reference = [{'number': '1', 'title': 'The Man Trap'}, {'number': '2', 'title': 'Charlie X'}, {'number': '3', 'title': 'Where No Man Has Gone Before'}, {'number': '4', 'title': 'The Naked Time'}, {'number': '5', 'title': 'The Enemy Within'}, {'number': '6', 'title': "Mudd's Women"}, {'number': '7', 'title': 'What Are Little Girls Made Of?'}, {'number': '8', 'title': 'Miri'}, {'number': '9', 'title': 'Dagger of the Mind'}, {'number': '10', 'title': 'The Corbomite Maneuver'}, {'number': '11', 'title': 'The Menagerie (1)'}, {'number': '12', 'title': 'The Menagerie (2)'}, {'number': '13', 'title': 'The Conscience of the King'}, {'number': '14', 'title': 'Balance of Terror'}, {'number': '15', 'title': 'Shore Leave'}, {'number': '16', 'title': 'The Galileo Seven'}, {'number': '17', 'title': 'The Squire of Gothos'}, {'number': '18', 'title': 'Arena'}, {'number': '19', 'title': 'Tomorrow Is Yesterday'}, {'number': '20', 'title': 'Court Martial'}, {'number': '21', 'title': 'The Return of the Archons'}, {'number': '22', 'title': 'Space Seed'}, {'number': '23', 'title': 'A Taste of Armageddon'}, {'number': '24', 'title': 'This Side of Paradise'}, {'number': '25', 'title': 'The Devil in the Dark'}, {'number': '26', 'title': 'Errand of Mercy'}, {'number': '27', 'title': 'The Alternative Factor'}, {'number': '28', 'title': 'The City on the Edge of Forever'}, {'number': '29', 'title': 'Operation: Annihilate!'}]

        self.assertEqual(episodes_reference, episodes)

    # tests for poster_path()
    def test_poster_path_original(self):
        poster_id = "mqGTDn6c5wy4Bwf6DR7eZeO7c5d"

        poster_path = API.poster_path(poster_id=poster_id, original_resolution=True)

        self.assertEqual(f"/t/p/original/{poster_id}.jpg", poster_path)

    def test_poster_path_94x141(self):
        poster_id = "mqGTDn6c5wy4Bwf6DR7eZeO7c5d"
        width = 94
        height = 141

        poster_path = API.poster_path(poster_id=poster_id, width=width, height=height)

        self.assertEqual(f"/t/p/w{width}_and_h{height}_bestv2/{poster_id}.jpg", poster_path)

    def test_poster_path_188x282(self):
        poster_id = "mqGTDn6c5wy4Bwf6DR7eZeO7c5d"
        width = 188
        height = 282

        poster_path = API.poster_path(poster_id=poster_id, width=width, height=height)

        self.assertEqual(f"/t/p/w{width}_and_h{height}_bestv2/{poster_id}.jpg", poster_path)

    def test_poster_path_150x225(self):
        poster_id = "mqGTDn6c5wy4Bwf6DR7eZeO7c5d"
        width = 150
        height = 225

        poster_path = API.poster_path(poster_id=poster_id, width=width, height=height)

        self.assertEqual(f"/t/p/w{width}_and_h{height}_bestv2/{poster_id}.jpg", poster_path)

    def test_poster_path_300x450(self):
        poster_id = "mqGTDn6c5wy4Bwf6DR7eZeO7c5d"
        width = 300
        height = 450

        poster_path = API.poster_path(poster_id=poster_id, width=width, height=height)

        self.assertEqual(f"/t/p/w{width}_and_h{height}_bestv2/{poster_id}.jpg", poster_path)

    def test_poster_path_600x900(self):
        poster_id = "mqGTDn6c5wy4Bwf6DR7eZeO7c5d"
        width = 600
        height = 900

        poster_path = API.poster_path(poster_id=poster_id, width=width, height=height)

        self.assertEqual(f"/t/p/w{width}_and_h{height}_bestv2/{poster_id}.jpg", poster_path)

    def test_poster_path_invalid_size(self):
        poster_id = "mqGTDn6c5wy4Bwf6DR7eZeO7c5d"
        width = 1000
        height = 2000

        self.assertRaises(ValueError, lambda: API.poster_path(poster_id=poster_id, width=width, height=height))

    # tests for TV.number_of_seasons()
    def test_number_of_seasons(self):
        self.assertEqual(3, API.TV.number_of_seasons(series_id="253"))


if __name__ == '__main__':
    unittest.main()
