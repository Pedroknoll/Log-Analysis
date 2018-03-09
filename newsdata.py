#!/usr/bin/env python3

""" Create database connection and congigure queries to asnwer some questions.
    The questions:
      1. What are the most popular three articles of all time?
      2. Who are the most popular article authors of all time?
      3. On which days did more than 1 percent of requests lead to errors?"""

import psycopg2

DBNAME = "newsdata"

# A method to perform a query in database
def make_query(query):
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    c.execute(query)
    return c.fetchall()
    db.close()

# 1. query to return the three most popular three articles of all time
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

# 2. query to return the most popular article authors of all time?
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

# 3. query on which days did more than 1% of requests lead to errors?
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
