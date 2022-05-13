import sqlite3

class Database:

    def __init__(self):
        self.__conn = self.__create__connection()

    def __create__connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = sqlite3.connect("../quiz-app-database.db")
        conn.isolation_level = None
        return conn

    def getCursor(self):
        return self.__conn.cursor()

    def close(self):
        self.__conn.close()

    def formatStr(self, string : str):
        """ format string for database insertion 
        :param string: value as string
        :return: formated string
        """
        return str(string).replace("'", "''").replace('"', '""')
