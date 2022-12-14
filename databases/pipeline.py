import psycopg2
import configparser as cp
import queries as q
from sqlite_example import connect_to_db, execute_q

config = cp.ConfigParser()
config.read('values.config')

# Connect to ElephantSQL
DB_NAME = config.get('ElephantSQL', 'DB_NAME')
USER = config.get('ElephantSQL', 'USER')
PWD = config.get('ElephantSQL', 'PWD')
HOST = config.get('ElephantSQL', 'HOST')
PORT = config.get('ElephantSQL', 'PORT')


def connect_to_pg(db=DB_NAME, user=USER, password=PWD, host=HOST):
    conn = psycopg2.connect(dbname=DB_NAME, user=USER,
                            password=PWD, host=HOST, port=PORT)
    curs = conn.cursor()
    return conn, curs


def modify_db(conn, curs, query):
    curs.execute(query)
    conn.commit()


if __name__ == '__main__':
    # Get data from SQLite
    sl_conn = connect_to_db()
    sl_characters = execute_q(sl_conn, q.GET_CHARACTERS)

    # Create destination table within PostgreSQL DB
    conn, curs = connect_to_pg()
    modify_db(conn, curs, q.DROP_CHARACTER_TABLE)
    modify_db(conn, curs, q.CREATE_CHARACTER_TABLE)

    # Loop over characters and insert into PostgreSQL with correct values
    for character in sl_characters:
        modify_db(conn, curs, f'''
            INSERT INTO characters ("name", "level", "exp", "hp",
            "strength", "intelligence", "dexterity", "wisdom")
            VALUES {str(character[1:])}
            ''')

    # modify_db(conn, curs, q.INSERT_RYAN)
