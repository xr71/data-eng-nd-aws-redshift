import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    This function takes in a cursor object from Redshift via the Psycopg2 library
    and a connection object. It runs through a series of DROP statements and 
    drops all of the tables in Redshift for this ETL pipeline should they exist.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    This function takes in a cursor object from Redshift via the Psycopg2 library
    and a connection object. It runs through a series of CREATE statements and 
    creates new tables based on the DDL in sql_queries.py 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Executes the previous ETL statements while orchestrating the config and 
    connection to Redshift.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
