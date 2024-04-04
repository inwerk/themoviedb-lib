# themoviedb-lib

Python library providing useful tools for [The Movie Database (TMDb)](https://www.themoviedb.org/) without depending on API-Keys 

## Features

- Comprehensive tools for retrieving movie / TV show data
- No dependence on API-Keys
- The data is web scraped from TMDb
- Focus on simplicity and functionality

### Installation

```sh
pip install themoviedb-lib
```

Or if you have multiple Python / pip versions installed, use `pip3`:

```sh
pip3 install themoviedb-lib
```

### Usage

Simple usage examples:

```py
import tmdb

# Search for 'Star Wars' movies and TV shows
search_results = tmdb.API.search(query="Star Wars")

# Display search results on the screen
for result in search_results:
    print(result)

# Download poster images for the search results
posters = []
for result in search_results:
    posters.append(result.poster())

# Display movies on the screen
for result in search_results:
    if result.is_movie():
        print(result)

# For every TV show display the episodes for the first season on the screen
for result in search_results:
    if result.is_tv() and "1" in result.seasons():
        print(result.episodes(season_id="1"))
```

### Utilities

| Method                            | Description                                    |
|-----------------------------------|------------------------------------------------|
| `tmdb.API.search()`               | Search for movies and TV shows                 |
| `tmdb.API.languages()`            | Get a list of languages supported by TMDb      |
| `tmdb.API.categories()`           | Get a list of categories supported by TMDb     |
| `tmdb.API.poster_path()`          | Generate a poster path for a movie / TV series |
| `tmdb.API.TV.seasons()`           | Get a list of seasons for a TV series          |
| `tmdb.API.TV.number_of_seasons()` | Get the season count for a TV series           |
| `tmdb.API.TV.episodes()`          | Get a list of episodes for a TV series season  |
| `tmdb.API...()`                   | MORE UTILITIES COMING SOON                     |
