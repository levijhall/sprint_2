import sqlite3
import pandas as pd
import queries as q

DEFAULT_DATABASE = 'buddymove_holidayiq.sqlite3'


def connect_to_db(db_name=DEFAULT_DATABASE):
    return sqlite3.connect(db_name)


def execute_q(conn, query):
    curs = conn.cursor()
    curs.execute(query)
    return curs.fetchall()


if __name__ == '__main__':
    conn = connect_to_db()
    df = pd.read_csv('buddymove_holidayiq.csv')
    df.to_sql('BuddyMove', conn, if_exists='replace')
    print(execute_q(conn, q.COUNT))
    print(execute_q(conn, q.COUNT_NATURE_SHOPPING_100))
    print(execute_q(conn, q.AVG_CATEGORIES))
