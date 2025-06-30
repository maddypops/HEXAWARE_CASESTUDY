class EmployeeNotFoundException(Exception):
    def __init__(self, message="Employee not found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'EmployeeNotFoundException: {self.message}'
