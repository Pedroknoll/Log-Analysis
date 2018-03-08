#!/usr/bin/env python3

""" Create database connection and congigure queries to asnwer some questions.
    The questions:
      1. What are the most popular three articles of all time?
      2. Who are the most popular article authors of all time?
      3. On which days did more than 1 percent of requests lead to errors?"""

import psycopg2

DBNAME = "newsdata"

# A method to performe a query in database
def make_query(query):
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    c.execute(query)
    return c.fetchall()
    db.close()

# 1. query to retrieve the most popular three articles of all timestamp
query_one = ("select title, count(title) as views"
                "from articles"
                "articles,log"
                "where concat('/article/',articles.slug) = log.path"
                "and log.status = '200 OK'"
                "group by articles.title"
                "order by views DESC"
                "limit 3";)
