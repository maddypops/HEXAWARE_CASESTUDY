import pyodbc
from Payxpert.exception.DatabaseConnectionException import DatabaseConnectionException

class DBConnUtil:
    @staticmethod
    def get_connection(connection_string):
        try:
            conn = pyodbc.connect(connection_string)
            return conn
        except pyodbc.Error as e:
            raise DatabaseConnectionException(f"Failed to establish a database connection: {e}")

    @staticmethod
    def close_connection(conn):
        try:
            if conn:
                conn.close()
        except pyodbc.Error as e:
            raise DatabaseConnectionException(f"Failed to close the database connection: {e}")
