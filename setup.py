from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Setting up
setup(
    name="themoviedb-lib",  # Required
    version="0.0.4",  # Required
    description="Library providing useful tools for The Movie Database (TMDb). Not dependent on API-keys.",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional
    url="https://github.com/inwerk/themoviedb-lib",  # Optional
    author="",  # Optional
    author_email="",  # Optional
    classifiers=[  # Optional (https://pypi.org/classifiers/)
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Build Tools"
    ],
    keywords=[  # Optional
        "tmdb", "themoviedb", "the movie database", "the movie db",
        "movie", "movies", "tv", "tv show", "tv shows"],
    packages=find_packages(),  # Required
    install_requires=['requests', 'beautifulsoup4', 'fake-useragent']  # Optional
)
