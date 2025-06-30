class FinancialRecordException(Exception):
    def __init__(self, message="Financial record error"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'FinancialRecordException: {self.message}'
