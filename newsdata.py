#!/usr/bin/env python3

""" Create database connection and congigure queries to asnwer some questions.
    The questions:
      1. What are the most popular three articles of all time?
      2. Who are the most popular article authors of all time?
      3. On which days did more than 1 percent of requests lead to errors?"""

import psycopg2
DBNAME = "news"


# Connect to Database. Return a database connection.
def connect():
    try:
        db = psycopg2.connect(dbname=DBNAME)
        c = db.cursor()
        return db, c
    except Exception:
        print('Unnable to conect to the database')


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
                SELECT date_trunc('day', time) AS date,
                COUNT(*) AS error_requests
                FROM log
                WHERE status like '%404%'
                GROUP BY date
                ) AS errors,
                (
                SELECT date_trunc('day', time) AS date,
                COUNT(*) AS requests
                FROM log
                GROUP BY date
                ) AS total
            WHERE errors.date = total.date
            AND (CAST(error_requests AS real)/total.requests) > 0.01
            ORDER BY percent DESC;
"""


# A method to perform a query in database
def get_results(query):
        db, c = connect()
        c.execute(query)
        results = c.fetchall()
        for i in results:
            print(i[0]),
            print("-"),
            print i[1]
        print("\n")
        db.close()
        return


# code only execute when the module is running as a program
if __name__ == "__main__":
    print("\033[7m1- The 3 most popular articles of all time are:\033[m\n")
    get_results(query_one)

    print("\033[7m2- The most popular article authors of all time are:"
            "\033[m\n")
    get_results(query_two)

    print("\033[7m3- Days with more than 1% of request that lead to an error"
            "\033[m\n")
    get_results(query_three)
