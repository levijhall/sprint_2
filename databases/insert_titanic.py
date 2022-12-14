import seaborn as sns
import numpy as np
import psycopg2
import configparser as cp

# Queries to be used in this script
DROP_TITANIC_TABLE = '''
DROP TABLE IF EXISTS titanic;
'''

DROP_PCLASS_ENUM = '''
DROP TYPE class_enum;
'''

CREATE_PCLASS_ENUM = '''
CREATE TYPE class_enum AS ENUM ('First', 'Second', 'Third');
'''

CREATE_TITANIC_TABLE = '''
CREATE TABLE IF NOT EXISTS titanic
(
    survived BOOLEAN NOT NULL,
    class class_enum NOT NULL,
    sex VARCHAR(7) NOT NULL,
    age INT,
    num_sibs_and_spouses INT NOT NULL,
    num_parents_and_children INT NOT NULL,
    fare REAL NOT NULL,
    embark_town VARCHAR(15) NOT NULL
);
'''

SURVIVAL_RATE_PER_SEX = '''
WITH
    male_survival AS
    (
        SELECT AVG(survived::int) AS rate
        FROM titanic
        WHERE sex = 'male'
    ),
    female_survival AS
    (
        SELECT AVG(survived::int) AS rate
        FROM titanic
        WHERE sex = 'female'
    )
    SELECT male_survival.rate, female_survival.rate
    FROM male_survival, female_survival
'''

# Load in secret credentials 🤐
config = cp.ConfigParser()
config.read('values.config')

DB_NAME = config.get('ElephantSQL', 'DB_NAME')
USER = config.get('ElephantSQL', 'USER')
PWD = config.get('ElephantSQL', 'PWD')
HOST = config.get('ElephantSQL', 'HOST')
PORT = config.get('ElephantSQL', 'PORT')

# Connect to ElephantSQL
conn = psycopg2.connect(dbname=DB_NAME, user=USER,
                        password=PWD, host=HOST, port=PORT)
curs = conn.cursor()


# Replace NaN with Null
def nan_to_null(value):
    if np.isnan(value):
        return 'NULL'
    return value


if __name__ == '__main__':
    # Load the Seaborn dataset
    titanic = sns.load_dataset('titanic')

    # Recreate tables and enums
    curs.execute(DROP_TITANIC_TABLE + DROP_PCLASS_ENUM)
    curs.execute(CREATE_PCLASS_ENUM + CREATE_TITANIC_TABLE)

    for index, row in titanic.iterrows():
        survived = row['survived'] == 1  # convert int to boolean
        pclass = row['class']
        sex = row['sex']
        age = nan_to_null(row['age'])  # convert any nans to nulls
        num_sibs_and_spouses = row['sibsp']
        num_parents_and_children = row['parch']
        fare = row['fare']
        embark_town = row['embark_town']

        values = f"""({survived}, '{pclass}', '{sex}', {age},
                     {num_sibs_and_spouses}, {num_parents_and_children},
                     {fare}, '{embark_town}')"""

        curs.execute(f'''
        INSERT INTO titanic ("survived", "class", "sex", "age",
        "num_sibs_and_spouses", "num_parents_and_children", "fare",
        "embark_town")
        VALUES {values}
        ''')

    conn.commit()

    curs.execute(SURVIVAL_RATE_PER_SEX)
    print(curs.fetchall())
