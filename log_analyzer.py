#!/bin/env python3

import psycopg2
from pprint import pprint
from os import linesep

ARTICLES_QUERY = """select articles.title, count(log.status) as views 
                    from articles 
                    left join log 
                    on articles.slug = split_part(log.path,'/',3) 
                    group by articles.title 
                    order by views desc;"""

AUTHOR_QUERY = """select authors.name, raw.views 
                  from authors 
                  left join (select articles.author as id, count(log.path) as views 
                             from articles 
                             left join log 
                             on articles.slug = split_part(log.path,'/',3) 
                             group by articles.author) as raw 
                  on authors.id = raw.id 
                  order by raw.views desc;"""

NOT_FOUND_QUERY = """select by_status.day 
                    from (select date(time) as day, count(status) as err 
                          from log 
                          where status!='200 OK' 
                          group by day) as by_status 
                    join (select date(time) as day, count(*) as requests 
                          from log 
                          group by day) as total 
                    on by_status.day = total.day 
                       and (100 * by_status.err) > total.requests;"""

def print_views(views_list):
    """Prettyprints result_list from cursor.fetchall()."""
    for item in views_list:
        print('{} - {} views'.format(item[0],item[1]))

if __name__ == '__main__':
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    print(linesep + "Most popular articles in descending order" + linesep)
    cursor.execute(ARTICLES_QUERY)
    print_views(cursor.fetchall())
    print(linesep + "Most popular authors in descending order" + linesep)
    cursor.execute(AUTHOR_QUERY)
    print_views(cursor.fetchall())
    print(linesep + "Days with more than 1% failed connections" + linesep)
    cursor.execute(NOT_FOUND_QUERY)
    print(str(cursor.fetchall()[0][0]) + linesep)
    cursor.close()
    db.close()
