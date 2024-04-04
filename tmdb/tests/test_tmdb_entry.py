import unittest
from .. import *


class TestTMDbEntry(unittest.TestCase):

    # tests for __str__()
    def test_string_representation(self):
        tmdb_entry = TMDbEntry(title="The Movie", release_year="2024")

        self.assertEqual("The Movie (2024)", str(tmdb_entry))

    def test_string_representation_no_release_year(self):
        tmdb_entry = TMDbEntry(title="The Movie")

        self.assertEqual("The Movie", str(tmdb_entry))

    def test_string_representation_no_title(self):
        tmdb_entry = TMDbEntry(release_year="2024")

        self.assertEqual("Not available", str(tmdb_entry))

    def test_string_representation_no_release_year_and_title(self):
        tmdb_entry = TMDbEntry()

        self.assertEqual("Not available", str(tmdb_entry))

    # tests for __eq__()
    def test_equals_same_entry(self):
        tmdb_entry_1 = TMDbEntry(category="movie", tmdb_id="1")
        tmdb_entry_2 = TMDbEntry(category="movie", tmdb_id="1")

        self.assertEqual(tmdb_entry_1, tmdb_entry_2)

    def test_equals_different_category(self):
        tmdb_entry_1 = TMDbEntry(category="movie", tmdb_id="1")
        tmdb_entry_2 = TMDbEntry(category="tv", tmdb_id="1")

        self.assertNotEqual(tmdb_entry_1, tmdb_entry_2)

    def test_equals_different_tmdb_id(self):
        tmdb_entry_1 = TMDbEntry(category="movie", tmdb_id="1")
        tmdb_entry_2 = TMDbEntry(category="movie", tmdb_id="2")

        self.assertNotEqual(tmdb_entry_1, tmdb_entry_2)

    def test_equals_empty_entry(self):
        tmdb_entry_1 = TMDbEntry()
        tmdb_entry_2 = TMDbEntry()

        self.assertEqual(tmdb_entry_1, tmdb_entry_2)

    # tests for category attribute
    def test_category_movie(self):
        tmdb_entry = TMDbEntry(category="movie")

        self.assertEqual("movie", tmdb_entry.category)

    def test_category_tv(self):
        tmdb_entry = TMDbEntry(category="tv")

        self.assertEqual("tv", tmdb_entry.category)

    def test_category_invalid_category(self):
        self.assertRaises(ValueError, lambda: TMDbEntry(category="invalid_category"))

    def test_category_invalid_type(self):
        self.assertRaises(TypeError, lambda: TMDbEntry(category=0))

    def test_category_none(self):
        tmdb_entry = TMDbEntry(category=None)

        self.assertIsNone(tmdb_entry.category)

    # tests for tmdb id attribute
    def test_tmdb_id_number(self):
        for x in range(1, 100, 5):
            tmdb_entry = TMDbEntry(tmdb_id=str(x))
            self.assertEqual(str(x), tmdb_entry.tmdb_id)

    def test_tmdb_id_invalid_type(self):
        self.assertRaises(TypeError, lambda: TMDbEntry(tmdb_id=0))

    def test_tmdb_id_non_numeric(self):
        self.assertRaises(ValueError, lambda: TMDbEntry(tmdb_id="x"))

    def test_tmdb_id_negative_number(self):
        self.assertRaises(ValueError, lambda: TMDbEntry(tmdb_id="-1"))

    def test_tmdb_id_zero(self):
        self.assertRaises(ValueError, lambda: TMDbEntry(tmdb_id="0"))

    def test_tmdb_id_none(self):
        tmdb_entry = TMDbEntry(tmdb_id=None)

        self.assertIsNone(tmdb_entry.tmdb_id)

    # tests for title attribute
    def test_title_string(self):
        tmdb_entry = TMDbEntry(title="The Movie")

        self.assertEqual("The Movie", tmdb_entry.title)

    def test_title_invalid_type(self):
        self.assertRaises(TypeError, lambda: TMDbEntry(title=0))

    def test_title_none(self):
        tmdb_entry = TMDbEntry(title=None)

        self.assertIsNone(tmdb_entry.title)

    # tests for release_year attribute
    def test_release_year_number(self):
        tmdb_entry = TMDbEntry(release_year="2024")

        self.assertEqual("2024", tmdb_entry.release_year)

    def test_release_year_invalid_type(self):
        self.assertRaises(TypeError, lambda: TMDbEntry(release_year=0))

    def test_release_year_non_numeric(self):
        self.assertRaises(ValueError, lambda: TMDbEntry(release_year="x"))

    def test_release_year_none(self):
        tmdb_entry = TMDbEntry(release_year=None)

        self.assertIsNone(tmdb_entry.release_year)

    # tests for description attribute
    def test_description_string(self):
        tmdb_entry = TMDbEntry(description="The Movie")

        self.assertEqual("The Movie", tmdb_entry.description)

    def test_description_invalid_type(self):
        self.assertRaises(TypeError, lambda: TMDbEntry(description=0))

    def test_description_none(self):
        tmdb_entry = TMDbEntry(description=None)

        self.assertIsNone(tmdb_entry.description)

    # tests for poster_id attribute
    def test_poster_id_string(self):
        tmdb_entry = TMDbEntry(poster_id="mqGTDn6c5wy4Bwf6DR7eZeO7c5d")

        self.assertEqual("mqGTDn6c5wy4Bwf6DR7eZeO7c5d", tmdb_entry.poster_id)

    def test_poster_id_invalid_type(self):
        self.assertRaises(TypeError, lambda: TMDbEntry(poster_id=0))

    def test_poster_id_none(self):
        tmdb_entry = TMDbEntry(poster_id=None)

        self.assertIsNone(tmdb_entry.poster_id)

    # tests for language attribute
    def test_language_string(self):
        tmdb_entry = TMDbEntry(language="en")

        self.assertEqual("en", tmdb_entry.language)

    def test_language_invalid_type(self):
        self.assertRaises(TypeError, lambda: TMDbEntry(language=0))

    def test_language_invalid_language_tag(self):
        self.assertRaises(ValueError, lambda: TMDbEntry(language="roman"))

    def test_language_none(self):
        tmdb_entry = TMDbEntry(language=None)

        self.assertIsNone(tmdb_entry.language)

    # tests for format_plex()
    def test_format_plex_string_representation(self):
        tmdb_entry = TMDbEntry(tmdb_id="1", title="The Movie", release_year="2024")

        self.assertEqual("The Movie (2024) {tmdb-1}", tmdb_entry.format_plex())

    def test_format_plex_string_representation_no_release_year(self):
        tmdb_entry = TMDbEntry(tmdb_id="1", title="The Movie")

        self.assertEqual("The Movie {tmdb-1}", tmdb_entry.format_plex())

    def test_format_plex_string_representation_no_title(self):
        tmdb_entry = TMDbEntry(tmdb_id="1", release_year="2024")

        self.assertEqual("Not available {tmdb-1}", tmdb_entry.format_plex())

    def test_format_plex_string_representation_no_release_year_and_title(self):
        tmdb_entry = TMDbEntry(tmdb_id="1")

        self.assertEqual("Not available {tmdb-1}", tmdb_entry.format_plex())

    def test_format_plex_string_representation_no_tmdb_id(self):
        tmdb_entry = TMDbEntry(title="The Movie", release_year="2024")

        self.assertEqual("The Movie (2024)", tmdb_entry.format_plex())

    def test_format_plex_string_representation_no_tmdb_id_and_release_year(self):
        tmdb_entry = TMDbEntry(title="The Movie")

        self.assertEqual("The Movie", tmdb_entry.format_plex())

    def test_format_plex_string_representation_no_tmdb_id_and_title(self):
        tmdb_entry = TMDbEntry(release_year="2024")

        self.assertEqual("Not available", tmdb_entry.format_plex())

    def test_format_plex_string_representation_no_tmdb_id_and_release_year_and_title(self):
        tmdb_entry = TMDbEntry()

        self.assertEqual("Not available", tmdb_entry.format_plex())

    # tests for is_movie()
    def test_is_movie_for_category_movie(self):
        tmdb_entry = TMDbEntry(category="movie")

        self.assertTrue(tmdb_entry.is_movie())

    def test_is_movie_for_category_tv(self):
        tmdb_entry = TMDbEntry(category="tv")

        self.assertFalse(tmdb_entry.is_movie())

    def test_is_movie_for_category_none(self):
        tmdb_entry = TMDbEntry(category=None)

        self.assertFalse(tmdb_entry.is_movie())

    # tests for is_tv()
    def test_is_tv_for_category_tv(self):
        tmdb_entry = TMDbEntry(category="tv")

        self.assertTrue(tmdb_entry.is_tv())

    def test_is_tv_for_category_movie(self):
        tmdb_entry = TMDbEntry(category="movie")

        self.assertFalse(tmdb_entry.is_tv())

    def test_is_tv_for_category_none(self):
        tmdb_entry = TMDbEntry(category=None)

        self.assertFalse(tmdb_entry.is_tv())

    # tests for poster()
    def test_poster_default_resolution(self):
        tmdb_entry = TMDbEntry(poster_id="mqGTDn6c5wy4Bwf6DR7eZeO7c5d")

        self.assertIsInstance(tmdb_entry.poster(), io.BytesIO)

    def test_poster_low_resolution(self):
        tmdb_entry = TMDbEntry(poster_id="mqGTDn6c5wy4Bwf6DR7eZeO7c5d")

        self.assertIsInstance(tmdb_entry.poster(resolution="low"), io.BytesIO)

    def test_poster_medium_resolution(self):
        tmdb_entry = TMDbEntry(poster_id="mqGTDn6c5wy4Bwf6DR7eZeO7c5d")

        self.assertIsInstance(tmdb_entry.poster(resolution="medium"), io.BytesIO)

    def test_poster_high_resolution(self):
        tmdb_entry = TMDbEntry(poster_id="mqGTDn6c5wy4Bwf6DR7eZeO7c5d")

        self.assertIsInstance(tmdb_entry.poster(resolution="high"), io.BytesIO)

    def test_poster_original_resolution(self):
        tmdb_entry = TMDbEntry(poster_id="mqGTDn6c5wy4Bwf6DR7eZeO7c5d")

        self.assertIsInstance(tmdb_entry.poster(resolution="original"), io.BytesIO)

    def test_poster_poster_id_is_none(self):
        tmdb_entry = TMDbEntry(poster_id=None)

        self.assertIsNone(tmdb_entry.poster())

    def test_poster_invalid_resolution(self):
        tmdb_entry = TMDbEntry(poster_id="mqGTDn6c5wy4Bwf6DR7eZeO7c5d")

        self.assertRaises(ValueError, lambda: tmdb_entry.poster(resolution="ultra-high"))

    # tests for seasons()
    def test_seasons(self):
        tmdb_entry = TMDbEntry(category="tv", tmdb_id="253")
        seasons_reference = ['0', '1', '2', '3']

        self.assertEqual(seasons_reference, tmdb_entry.seasons())

    def test_seasons_movie(self):
        tmdb_entry = TMDbEntry(category="movie", tmdb_id="11")
        self.assertRaises(Exception, lambda: tmdb_entry.seasons())

    # tests for episodes()
    def test_episodes(self):
        tmdb_entry = TMDbEntry(category="tv", tmdb_id="253")
        episodes_reference = [{'number': '1', 'title': 'The Man Trap'}, {'number': '2', 'title': 'Charlie X'}, {'number': '3', 'title': 'Where No Man Has Gone Before'}, {'number': '4', 'title': 'The Naked Time'}, {'number': '5', 'title': 'The Enemy Within'}, {'number': '6', 'title': "Mudd's Women"}, {'number': '7', 'title': 'What Are Little Girls Made Of?'}, {'number': '8', 'title': 'Miri'}, {'number': '9', 'title': 'Dagger of the Mind'}, {'number': '10', 'title': 'The Corbomite Maneuver'}, {'number': '11', 'title': 'The Menagerie (1)'}, {'number': '12', 'title': 'The Menagerie (2)'}, {'number': '13', 'title': 'The Conscience of the King'}, {'number': '14', 'title': 'Balance of Terror'}, {'number': '15', 'title': 'Shore Leave'}, {'number': '16', 'title': 'The Galileo Seven'}, {'number': '17', 'title': 'The Squire of Gothos'}, {'number': '18', 'title': 'Arena'}, {'number': '19', 'title': 'Tomorrow Is Yesterday'}, {'number': '20', 'title': 'Court Martial'}, {'number': '21', 'title': 'The Return of the Archons'}, {'number': '22', 'title': 'Space Seed'}, {'number': '23', 'title': 'A Taste of Armageddon'}, {'number': '24', 'title': 'This Side of Paradise'}, {'number': '25', 'title': 'The Devil in the Dark'}, {'number': '26', 'title': 'Errand of Mercy'}, {'number': '27', 'title': 'The Alternative Factor'}, {'number': '28', 'title': 'The City on the Edge of Forever'}, {'number': '29', 'title': 'Operation: Annihilate!'}]

        self.assertEqual(episodes_reference, tmdb_entry.episodes(season_id="1"))

    def test_episodes_movie(self):
        tmdb_entry = TMDbEntry(category="movie", tmdb_id="11")
        self.assertRaises(Exception, lambda: tmdb_entry.episodes(season_id="1"))


if __name__ == '__main__':
    unittest.main()
