# Log Analyzation for Udacity

This is a small python script which prints diagnostics
for the news database. The output of the program can be
found in [RESULTS.txt](./RESULTS.txt).

## Dependencies
You need to have a current version of python3 and psycopg2
installed in order to run it. Furthermore, PostgreSQL needs
to be installed and running. Download the database data from [newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Unzip it and run
```
psql -d news -f newsdata.sql
```

## Usage
Simply execute log_analyzer.py, which is located at the
top level of the repository. E.g. on Unix, simply type
```
./log_analyzer.py
```