import sqlite3

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect("../quiz-app-database.db")
        conn.isolation_level = None
        return conn
    except BaseException as e:
        print(e)

    return None

def create_question(conn, question):
    """
    Create a new question into the questions table
    :param conn:
    :param question:
    :return: question id
    """
    cur = conn.cursor()

    try:
        # start transaction
        cur.execute("begin")

        insertion_result = cur.execute(
            f"INSERT INTO Question (Title, Text, Image) VALUES"
            f"('{formatStr(question.title)}', '{formatStr(question.text)}', '{question.image}')"
        )

        #send the request
        cur.execute("commit")

        return cur.lastrowid
    except BaseException as e:
        #in case of exception, roolback the transaction
        cur.execute('rollback')


def formatStr(string : str):
    """ format string for database insertion 
    :param string: value as string
    :return: formated string
    """
    return string.replace("'", "''")
