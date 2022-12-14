# Step 0 - import sqlite3
import sqlite3
import queries as q
import pandas as pd

DEFAULT_DATABASE = 'rpg_db.sqlite3'


# DB Connect function
def connect_to_db(db_name=DEFAULT_DATABASE):
    return sqlite3.connect(db_name)


def execute_q(conn, query):
    curs = conn.cursor()
    curs.execute(query)
    return curs.fetchall()


if __name__ == '__main__':
    conn = connect_to_db()
    # print(execute_q(conn, q.SELECT_ALL)[:5])
    results = execute_q(conn, q.AVG_ITEM_WEIGHT_PER_CHARACTER)
    df = pd.DataFrame(results)
    df.columns = ['name', 'average_item_weight']
    df.to_csv('rpg_db.csv', index=False)
    print(df.head())
