#!/usr/bin/env python3

""" This script prints out diagnostic information from the news database."""

from os import linesep
import psycopg2

ARTICLES_QUERY = """select articles.title, count(log.status) as views
                    from articles
                    left join log
                    on articles.slug = split_part(log.path,'/',3)
                    group by articles.title
                    order by views desc
                    limit 3;"""

AUTHOR_QUERY = """select authors.name, raw.views
                  from authors
                  left join (select articles.author as id
                             , count(log.path) as views
                             from articles
                             left join log
                             on articles.slug = split_part(log.path,'/',3)
                             group by articles.author) as raw
                  on authors.id = raw.id
                  order by raw.views desc;"""

NOT_FOUND_QUERY = """select to_char(by_status.day, 'Mon DD,YYYY')
                     , trunc((100.0 * by_status.err) / total.requests,2)
                     from (select date(time) as day, count(status) as err
                          from log
                          where status!='200 OK'
                          group by day) as by_status
                     join (select date(time) as day, count(*) as requests
                          from log
                          group by day) as total
                     on by_status.day = total.day
                       and (100 * by_status.err) > total.requests;"""


def print_result(result_list, suffix):
    """Prettyprints result_list with 2 colums from cursor.fetchall()
       and appends suffix for each row."""
    for item in result_list:
        print('{} - {} '.format(item[0], item[1]) + suffix)


if __name__ == '__main__':

    # Open connection to database and get a cursor.
    db = psycopg2.connect("dbname=news")
    curs = db.cursor()

    print(linesep + "Most popular articles in descending order" + linesep)
    curs.execute(ARTICLES_QUERY)
    print_result(curs.fetchall(), "views")

    print(linesep + "Most popular authors in descending order" + linesep)
    curs.execute(AUTHOR_QUERY)
    print_result(curs.fetchall(), "views")

    print(linesep + "Days with more than 1% failed connections" + linesep)
    curs.execute(NOT_FOUND_QUERY)
    print_result(curs.fetchall(), "% errors")

    # Close database cursor and connection.
    curs.close()
    db.close()
