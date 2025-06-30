class DatabaseConnectionException(Exception):
    """Exception raised for errors related to database connections."""

    def __init__(self, message="Error establishing or maintaining a database connection"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"DatabaseConnectionException: {self.message}"
