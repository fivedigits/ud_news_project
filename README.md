# Log Analysation for Udacity

This is a small python script which prints diagnostics
for the news database. The output of the program can be
found in [RESULTS.txt](./RESULTS.txt).

## Dependencies
You need to have a current version of python3 and psycopg2
installed in order to run it. Furthermore, PostgreSQL needs
to be installed and running. There must be a database
named *news* containing the data supplied by Udacity.

## Usage
Simply execute log_analyzer.py, which is located at the
top level of the repository. E.g. on Unix, simply type
```
./log_analyzer.py
```