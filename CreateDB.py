import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except ConnectionError:
        print("Unable to create connection")

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """


    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except:
        print("Unable to create table")

def create_tables():
    database = r"precious.db"

    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        userid integer PRIMARY KEY AUTOINCREMENT,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        email text NOT NULL,
                                        display_name text NOT NULL,
                                        password text NOT NULL
                                    ); """

    sql_create_category_table = """ CREATE TABLE IF NOT EXISTS category (
                                        categoryid integer PRIMARY KEY AUTOINCREMENT,
                                        category_name text NOT NULL,
                                        category_desc text NOT NULL
                                    ); """

    sql_create_item_table = """CREATE TABLE IF NOT EXISTS item (
                                    itemid integer PRIMARY KEY AUTOINCREMENT,
                                    item_name text NOT NULL,
                                    filename text NOT NULL,
                                    item_desc text NOT NULL,
                                    price real NOT NULL,
                                    userid integer NOT NULL,
                                    categoryid integer NOT NULL,
                                    FOREIGN KEY (userid) REFERENCES user (userid),
                                    FOREIGN KEY (categoryid) REFERENCES category (categoryid)
                                );"""

    sql_create_cart_table = """ CREATE TABLE IF NOT EXISTS cart (
                                    cartid integer PRIMARY KEY AUTOINCREMENT,
                                    userid integer,
                                    FOREIGN KEY (userid) REFERENCES user (userid)
                                ); """

    sql_create_cartdetails_table = """ CREATE TABLE IF NOT EXISTS cartdetails (
                                    cartdetailsid integer PRIMARY KEY AUTOINCREMENT,
                                    itemid integer NOT NULL,
                                    quantity integer NOT NULL,
                                    extended_price real NOT NULL,
                                    cartid integer NOT NULL,
                                    FOREIGN KEY (itemid) REFERENCES item (itemid),
                                    FOREIGN KEY (cartid) REFERENCES cart (cartid)
                                );"""


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create user table
        create_table(conn, sql_create_user_table)

        # create category table
        create_table(conn, sql_create_category_table)

        # create item table
        create_table(conn, sql_create_item_table)

        # create cart table
        create_table(conn, sql_create_cart_table)

        # create cartdetails table
        create_table(conn, sql_create_cartdetails_table)

    else:
        print("Error! cannot create the database connection.")



create_tables()