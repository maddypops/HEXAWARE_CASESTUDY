class PayrollGenerationException(Exception):
    def __init__(self, message="Error generating payroll"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'PayrollGenerationException: {self.message}'
