#
# File: objecttier.py
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, row):
    self._Movie_ID = row[0]
    self._Title = row[1]
    self._Release_Year = row[2]

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self, row):
    self._Movie_ID = row[0]
    self._Title = row[1]
    self._Release_Year = row[2]
    self._Num_Reviews = row[3]
    self._Avg_Rating = row[4]

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self, row):
    self._Movie_ID = row[0]
    self._Title = row[1]
    self._Release_Date = row[2]
    self._Runtime = row[3]
    self._Original_Language = row[4]
    self._Budget = row[5]
    self._Revenue = row[6]
    self._Num_Reviews = row[7]
    self._Avg_Rating = row[8]
    self._Tagline = row[9]
    self._Genres = row[10]
    self._Production_Companies = row[11]

  @property
  def Movie_ID(self):
    return self._Movie_ID
  
  @property
  def Title(self):
    return self._Title
  
  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue
  
  @property
  def Num_Reviews(self):
    return self._Num_Reviews
  
  @property
  def Avg_Rating(self):
    return self._Avg_Rating

  @property
  def Tagline(self):
    return self._Tagline

  @property
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  # Sql text for grabbing data from Movies
  sql= """Select Count(Movie_ID) From Movies;"""
  data = datatier.select_one_row(dbConn, sql)
  if len(data) == 0:
    return -1
  return data[0]


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  # Sql text for grabbing data from Ratings
  sql= """Select Count(Rating) From Ratings;"""
  data = datatier.select_one_row(dbConn, sql)
  if len(data) == 0:
    return -1
  return data[0]


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  movies = []
  # Sql text for grabbing data from Movies
  sql = """Select Movie_ID, Title, strftime('%Y', Release_Date)
           From Movies
           Where Title like '{0}'
           group by Title
           order by Title asc;"""
  sql = sql.format(pattern)
  data = datatier.select_n_rows(dbConn, sql)

  for row in data:
    movie = Movie(row)
    movies.append(movie)
  return movies


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  genres = []
  companies = []
  # Sql text for grabbing data from Movies and Ratings
  sql1 = """Select Movies.Movie_ID, Movies.Title,
           strftime('%Y-%m-%d', Movies.Release_Date),
           Movies.Runtime, Movies.Original_Language,
           Movies.Budget, Movies.Revenue,
           Count(Ratings.Rating), Avg(Ratings.Rating)
           From Movies Join Ratings On
           (Movies.Movie_ID = Ratings.Movie_ID)
           Where Movies.Movie_ID = '{0}';"""
  sql1 = sql1.format(movie_id)
  sql2 = """Select Tagline From Movie_Taglines
            Where Movie_ID = '{0}';"""
  sql2 = sql2.format(movie_id)
  # Sql text for grabbing data on Genres of specified movie
  sql3 = """Select Genres.Genre_Name
            From Movie_Genres Join Genres On
            (Movie_Genres.Genre_ID = Genres.Genre_ID)
            Where Movie_Genres.Movie_ID = '{0}';"""
  sql3 = sql3.format(movie_id)
  # Sql text for grabbing data on Companies of specified movie
  sql4 = """Select Companies.Company_Name
            From Movie_Production_Companies Join Companies on
            (Movie_Production_Companies.Company_ID = Companies.Company_ID)
            Where Movie_Production_Companies.Movie_ID = '{0}';"""
  sql4 = sql4.format(movie_id)
  aggData = []
  data1 = datatier.select_one_row(dbConn, sql1)
  if len(data1) == 0 or data1[0] == None:
    return None
  else:
    for i in data1:
      aggData.append(i)
    data2 = datatier.select_one_row(dbConn, sql2)
    data3 = datatier.select_n_rows(dbConn, sql3)
    data4 = datatier.select_n_rows(dbConn, sql4)
    # create list out of data for genres
    for row in data3:
      genres.append(row[0])
    # create list out of data for companies
    for row in data4:
      companies.append(row[0])
    # add genres and companies to the end of data1
    aggData.append(data2[0])
    aggData.append(genres)
    aggData.append(companies)
    return MovieDetails(aggData)
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  movies = []
  # Sql text for grabbing data From Movies and Ratings
  sql = """Select Movies.Movie_ID, Movies.Title, 
           strftime('%Y', Movies.Release_Date),
           Count(Ratings.Rating) As NumReviews,
           Avg(Ratings.Rating) As Avg_Rating
           From Movies Join Ratings On
           (Movies.Movie_ID = Ratings.Movie_ID)
           Group by Movies.Movie_ID
           Having NumReviews >= {0}
           order by Avg_Rating desc
           limit {1};"""
  sql = sql.format(min_num_reviews, N)
  data = datatier.select_n_rows(dbConn, sql)
  for row in data:
    movie = MovieRating(row)
    movies.append(movie)
  return movies


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  # Sql statement for checking movie_id in database
  sqlCheck = """Select Title From Movies
                Where Movie_ID = {0}"""
  sqlCheck = sqlCheck.format(movie_id)
  data = datatier.select_one_row(dbConn, sqlCheck)
  if len(data) > 0:
    # Sql statement for inserting rating into ratings database
    sqlInsert = """Insert Into Ratings(Movie_ID, Rating)
                               Values({0}, {1});"""
    sqlInsert = sqlInsert.format(movie_id, rating)
    if datatier.perform_action(dbConn, sqlInsert) == 1:
      return 1
  return 0


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  # Sql statement for checking movie_id in database
  sqlCheck = """Select Title From Movies
                Where Movie_ID = {0}"""
  sqlCheck = sqlCheck.format(movie_id)
  data = datatier.select_one_row(dbConn, sqlCheck)
  if len(data) > 0:
    # Sql statement for checking that a tagline already exists
    sqlCheck = """Select Tagline From Movie_Taglines
                  Where Movie_ID = {0}"""
    sqlCheck = sqlCheck.format(movie_id)
    data = datatier.select_one_row(dbConn, sqlCheck)
    if len(data) == 0:
      sqlInsert = """Insert Into 
                     Movie_Taglines(Movie_ID, Tagline)
                     Values({0}, {1});"""
      sqlInsert = sqlInsert.format(movie_id, tagline)
      if datatier.perform_action(dbConn, sqlInsert) == 1:
        return 1
    else:
      sqlUpdate = """Update Movie_Taglines
                     Set Tagline = '{0}'
                     Where Movie_ID = {1};"""
      sqlUpdate = sqlUpdate.format(tagline, movie_id)
      if datatier.perform_action(dbConn, sqlUpdate) == 1:
        return 1
  return 0