#
# Program to analyze data from MovieLens 
# This is a simplified version of the program for Project 01,
#
# Original author:
#   Jordan Fanapour
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#
# References: 
#  learning python: https://www.w3schools.com/python/
#  sqlite programming: https://docs.python.org/3/library/sqlite3.html
#
import sqlite3
import objecttier


#
# General Movie stats
#          
def getGeneralStats(dbConn):
  numMovies = objecttier.num_movies(dbConn)
  numReviews = objecttier.num_reviews(dbConn)
  print("General stats:")
  print("  # of movies:", f"{numMovies:,}")
  print("  # of reviews:", f"{numReviews:,}")

#
# Get_movies by partial name
#
def get_movies(dbConn):
    print()
    name = input("Enter movie name (wildcards _ and % supported): ")

    movies = objecttier.get_movies(dbConn, name)
    print()
    if movies is None:  # error
        print("**Internal error: get_movies")
    else:
      print("# of movies found:", len(movies))
      if len(movies) > 100:
        print()
        print("There are too many movies to display,",
        "please narrow your search and try again...")
      elif len(movies) != 0:
        print()
        for m in movies:
            print(m.Movie_ID, ":", 
                  m.Title,
                  f"({m.Release_Year})")


#
# Get_movies_details by partial movie_id
#
def get_movie_details(dbConn):
  print()
  name = input("Enter movie id: ")

  movie = objecttier.get_movie_details(dbConn, name)
  print()
  if movie is None:
    print("No such movie...")
  else:
    genreStr = ""
    companyStr = ""
    for g in movie.Genres:
      genreStr = genreStr + str(g) + ", "
    for c in movie.Production_Companies:
      companyStr = companyStr + str(c) + ", "
    print(movie.Movie_ID, ":", movie.Title)
    print("  Release date:", movie.Release_Date)
    print("  Runtime:", movie.Runtime, "(mins)")
    print("  Orig language:", movie.Original_Language)
    print("  Budget:", f"${movie.Budget:,}", "(USD)")
    print("  Revenue:", f"${movie.Revenue:,}", "(USD)")
    print("  Num reviews:", movie.Num_Reviews)
    print("  Avg rating:", f"{movie.Avg_Rating:.2f}", "(0..10)")
    print("  Genres:", genreStr)
    print("  Production companies:", companyStr)
    print("  Tagline:", movie.Tagline)

#
# Get top N movies with minimum number of reviews
#
def get_Top_N_Movies(dbConn):
  print()
  n = int(input("N? "))
  # Check valid input range for N
  if n <= 0:
    print("Please enter a positive value for N...")
    return
  minNum = int(input("min number of reviews? "))
  # check valid input range for minimum number of reviews
  if minNum <= 0:
    print("Please enter a positive value for min number of reviews...")
    return

  movies = objecttier.get_top_N_movies(dbConn, n, minNum)
  if len(movies) > 0:
    print()
    for movie in movies:
      print(movie.Movie_ID, ":",
            movie.Title, f"({movie.Release_Year}),",
            f"avg rating = {movie.Avg_Rating:.2f}",
            f"({movie.Num_Reviews} reviews)")

#
# Prompts user to insert rating and movie id
#
def insert_review(dbConn):
  print()
  rating = int(input("Enter rating (0..10): "))
  # Check for valid rating value
  if rating < 0 or rating > 10:
    print("Invalid rating...")
    return
  movie_id = int(input("Enter movie id: "))

  result = objecttier.add_review(dbConn, movie_id, rating)
  print()
  # Check to see if movie review was added
  if result == 0:
    print("No such movie...")
  else:
    print("Review successfully inserted")

#
# Prompts user to insert tagline and movie id
#
def insert_tagline(dbConn):
  print()
  tagline = input("tagline? ")
  movie_id = int(input("movie id? "))

  result = objecttier.set_tagline(dbConn, movie_id, tagline)
  print()
  # Check to see if movie review was added
  if result == 0:
    print("No such movie...")
  else:
    print("Tagline successfully set")


##################################################################  
#
# main
#

dbConn = sqlite3.connect('MovieLens.db')
print('** Welcome to the MovieLens app **')
print()
getGeneralStats(dbConn)
print()
cmd = input("Please enter a command (1-5, x to exit): ")

while cmd != "x":
    if cmd == "1":
      get_movies(dbConn)
    elif cmd == "2":
      get_movie_details(dbConn)
    elif cmd == "3":
      get_Top_N_Movies(dbConn)
    elif cmd == "4":
      insert_review(dbConn)
    elif cmd == "5":
      insert_tagline(dbConn)
    else:
        print("**Error, unknown command, try again...")

    print()
    cmd = input("Please enter a command (1-5, x to exit): ")

#
# done
#