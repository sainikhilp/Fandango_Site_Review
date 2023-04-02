# Fandango_Site_Review
Is there a conflict of interest for a website that both sells movie tickets     and displays movie ratings ?       More specifically does a website like Fandango artificially display higher      review ratings to sell more movie tickets?

Data : Fandango website data of year 2015

Fandango has two rating methods 
stars : visual
rating : numeric


To understand how fandango operates, read the below mentioned article.
Be cautious of online movie rating, especially Fandango's
There are two csv files:
-	One with fanango star ratings(fandango_scrape.csv)
-	One with other site ratings such as IMDb, Rotten Tomatoes, Metacritics etc.(all_sites_scores.csv)


All_sites_scores.csv
Column | Definition
   --- | -----------
FILM | The film in question
RottenTomatoes | The Rotten Tomatoes Tomatometer score  for the film
RottenTomatoes_User | The Rotten Tomatoes user score for the film
Metacritic | The Metacritic critic score for the film
Metacritic_User | The Metacritic user score for the film
IMDB | The IMDb user score for the film
Metacritic_user_vote_count | The number of user votes the film had on Metacritic
IMDB_user_vote_count | The number of user votes the film had on IMDb

Fandango_scrape.csv
Column | Definiton
FILM | The movie
STARS | Number of stars presented on Fandango.com
RATING |  The Fandango ratingValue for the film, as pulled from the HTML of each page. This is the actual average score the movie obtained.
VOTES |  number of people who had reviewed the film at the time we pulled it.


The analysis is divided into 3 parts: 
	p1: Understanding the background and data
	p2: Exploring Fandango displayed scores versus true user ratings
	p3: Comparison of Fandango’s ratings to other sites

Detailed analysis is available in doc file named analysis.

