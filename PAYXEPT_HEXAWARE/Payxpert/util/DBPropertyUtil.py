import configparser




class DBPropertyUtil:
    @staticmethod
    def get_connection_string():
        config = configparser.ConfigParser()
        config.read('dbconfig.ini')

        try:
        #    driver = config['Database']['Driver']
        #   server = config['Database']['Server']
        #   database = config['Database']['Database']
        #   trusted_connection = config['Database']['Trusted_Connection']

            conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;Database=EmployeeManagementDB;Trusted_Connection=yes;'
            return conn_string
        except KeyError as e:
            raise Exception(f"Error reading connection properties: {e}")
