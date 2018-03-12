#!/usr/bin/env python3

""" Create database connection and congigure queries to asnwer some questions.
    The questions:
      1. What are the most popular three articles of all time?
      2. Who are the most popular article authors of all time?
      3. On which days did more than 1 percent of requests lead to errors?"""

import psycopg2
from sys import exit
DBNAME = "news"


# 1. query to return the three most popular articles of all time
query_one = """
            SELECT title, COUNT(title) AS views
            FROM articles
            articles, log
            WHERE concat('/article/', articles.slug) = log.path
            AND log.status LIKE '%200%'
            GROUP BY articles.title
            ORDER BY views DESC
            LIMIT 3;
            """

# 2. query to return the most popular article authors of all time
query_two = """
            SELECT authors.name, COUNT(articles.author) as views
            FROM articles
            articles, log, authors
            WHERE concat('/article/', articles.slug) = log.path
            AND log.status LIKE '%200%'
            AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY views DESC;
            """

# 3. query on which days did more than 1% of requests lead to errors
query_three = """
            SELECT total.date,
                (CAST(error_requests AS real)/total.requests)
                AS percent
            FROM (
                SELECT CAST(date_trunc('day', time) AS date) AS date,
                COUNT(*) AS error_requests
                FROM log
                WHERE status like '%404%'
                GROUP BY date
                ) AS errors,
                (
                SELECT CAST(date_trunc('day', time) AS date) AS date,
                COUNT(*) AS requests
                FROM log
                GROUP BY date
                ) AS total
            WHERE errors.date = total.date
            AND (CAST(error_requests AS real)/total.requests) > 0.01
            ORDER BY percent DESC;
"""


def connect():
    """Connect to Database. Return a database connection."""
    try:
        db = psycopg2.connect(dbname=DBNAME)
        c = db.cursor()
        return db, c
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit(1)


def get_results(query):
    """A method to perform a query in database"""
    db, c = connect()
    c.execute(query)
    results = c.fetchall()
    return results
    db.close()


def print_results(query):
    results = get_results(query)
    for i in results:
        if isinstance(i[1], int) is True:
            print("{} - {:,} views".format(i[0], i[1]))
        else:
            print("{} - {:.2f} %".format(i[0], i[1] * 100))
    print("\n")


if __name__ == "__main__":
    """code only execute when the module is running as a program"""
    print("\033[7m1- The 3 most popular articles of all time are:\033[m\n")
    get_results(query_one)
    print_results(query_one)

    print("\033[7m2- The most popular article authors of all time are:"
          "\033[m\n")
    get_results(query_two)
    print_results(query_two)

    print("\033[7m3- Days with more than 1% of request that lead to an error"
          "\033[m\n")
    get_results(query_three)
    print_results(query_three)
