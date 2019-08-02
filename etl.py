import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    This function takes in a cursor object from Redshift via the Psycopg2 library
    and a connection object. It runs through a series of COPY statements and loads
    data from S3 into staging tables in Redshift. 
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    This function takes in a cursor object from Redshift via the Psycopg2 library
    and a connection object. It runs through a series of INSERT statements that 
    takes data from the staging tables and creates the star-schema tables for 
    the warehouse. 
    """
    for query in insert_table_queries:
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
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
