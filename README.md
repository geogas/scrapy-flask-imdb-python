Project Description
===================
That is a simple Python project illustrating the use of the following:

1. Scrapy (scraping and crawling framework)
1. Flask (micro web development framework based on Werkzeug)

The project is split up into two subprojects located in the respective folders.
We firstly scrape the Internet Movie Database (imdb) with the aim to get
information for movies we are interesting in. This information is persistenly
stored in the mongodb database. Given that a movie can be represented as a
document, mongodb was considered the best match for that use case. The second
subproject corresponds to a web application being responsible for rendering the
data we gathered from imdb.

Prerequisites
-------------
Before you start playing around with the projects make sure you have already
installed the dependencies.

Mongodb setup
-------------

###scrapy\_imdb

Location: scrapy\_imdb

Goal of our scraping application is to fetch information about movies. For
example: name, rating, genre, cast, etc. We specify a url that corresponds to a
list assembled by imdb itself, or by a user. E.g. top-250 movies
(http://www.imdb.com/chart/top). Then the scrapy spider parses this list and for
every movie existing there it acquires information. This information is later
being stored to imdb.movies collection of mongodb database by the implemented
pipeline.



###flask\_imdb

Location: flask\_imdb

A web application was implemented to present the aforementioned movie related
information in a human friendly manner. This application is backed up by a
server provided by the flask framework. Server listens for user requests and
dispatces these requests to the corresponding views. A sidebar allowing for
predefined queries exists. The user can also issue a request to the server by
typing a movie's name (or part of it, a rating (1-10), a desired genre (e.g.
crime), or a specific year.

Filling out mongodb collection
------------------------------
'''
cd scrappy\_flask\_imdb/scrappy\_imdb
scrapy crawl imdb
'''

This opetation will take some time and after its execution a number of movies
will exist in the movies collection of the imdb mongodb.

Starting the flask server
-------------------------
Once spider and pipeline have completed, the server can be started and content
can be served to the user via the web browser. In order to start the server
simply type:

'''
cd scrappy\_flask\_imdb/flask\_imdb/
python manage.py runserver
'''

Check web page
--------------
Open your preferred browser and type in the location bar:
'''
http://localhost:5000/index
'''

Cleanup
-------
Execute the following commands for dropping the movies collection:
'''javascript
mongo
use imdb
db.movies.drop()
'''

For dropping the whole imdb database please execute:
'''javascript
mongo
use imdb
db.dropDatabase()
'''
