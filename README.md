# Web Scraping Capstone using BeautifulSoup

This project is one of the Algoritma Academy Data Analytics Specialization's Capstone Project. In this project, I am learning how to do web scraping, a method for collecting data directly from a website, using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library. I tried to retrieve movies' information from [IMDB](https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31), a website especially designed for people to explore the world of movies and shows with millions of movies, TV, and entertainment programs in its database. The goal in this project is to be able to extract the information directly from the site, conduct an analysis on the most popular movies in 2021, and create a simple [Flask](https://flask.palletsprojects.com/en/2.0.x/) dashboard to present the result. This project is made for educational purpose.

## Dependencies

The packages required in this project is provided in `requirements.txt` file.

## Steps Taken in This Project

1. Create a function to obtain `Title`, `IMDB Rating`, `Metascore`, and `Votes` from a single IMDB website page.
2. Using iteration to obtain 1.000 movies' data from multiple pages.
3. Transform the obtained data into Pandas dataframe and data cleaning.
4. Perform analysis and visualization on the data.
5. Create a simple Flask dashboard based on the analysis result.
