#!/bin/env python3

import psycopg2
from pprint import pprint

ARTICLES_QUERY = """select articles.title, count(log.status) as views 
                    from articles left join log 
                    on articles.slug = split_part(log.path,'/',3) 
                    group by articles.title 
                    order by views desc;"""

if __name__ == '__main__':
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    print("Articles -- Views")
    cursor.execute(ARTICLES_QUERY)
    pprint(cursor.fetchall())
    cursor.close()
    db.close()
