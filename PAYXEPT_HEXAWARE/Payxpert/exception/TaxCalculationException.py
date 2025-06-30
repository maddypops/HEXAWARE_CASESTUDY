class TaxCalculationException(Exception):
    def __init__(self, message="Error calculating tax"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'TaxCalculationException: {self.message}'
