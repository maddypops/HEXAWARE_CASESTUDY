# dao/DatabaseContext.py

import pyodbc

class DatabaseContext:
    def __init__(self, conn_string):
        self.conn_string = conn_string
        self.conn = None

    def connect(self):
        """Establishes a database connection."""
        try:
            self.conn = pyodbc.connect(self.conn_string)
            print("Database connection established.")
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        """Executes a SQL query and returns the results."""
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")
            return None

    def execute_non_query(self, query, params=None):
        """Executes a non-query SQL command (like INSERT, UPDATE, DELETE)."""
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
        except pyodbc.Error as e:
            print(f"Error executing non-query: {e}")

    def get_connection(self):
        pass


# Usage example:
if __name__ == "__main__":
    conn_string = ('DRIVER={ODBC Driver 17 for SQL Server};'
                   'SERVER=MADDYPOPS;'
                   'Database=payroll;'
                   'Trusted_Connection=yes;')
    db_context = DatabaseContext(conn_string)
    db_context.connect()

    # Example of executing a query
    results = db_context.execute_query("SELECT * FROM Employee")
    for row in results:
        print(row)

    # Close the database connection
    db_context.close()
