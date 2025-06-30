import unittest
from unittest.mock import MagicMock
from Payxpert.dao.TaxServiceImpl import TaxServiceImpl

class TestVerifyTaxCalculationForHighIncome(unittest.TestCase):

    def setUp(self):
        # Mock the connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Instantiate TaxServiceImpl with the mocked connection
        self.tax_service = TaxServiceImpl(self.mock_conn)

    def test_verify_tax_calculation_for_high_income(self):
        emp_id = 1  # Example employee ID
        high_income = 100000.00  # High income example
        tax_rate = 30.0  # Assume a tax rate of 30%

        # Set up the mock to return the tax rate from the database
        self.mock_cursor.fetchone.return_value = [tax_rate]

        # Call the method to test
        tax = self.tax_service.calculate_tax_test(emp_id, high_income)

        # Expected tax value based on the mock tax rate and income
        expected_tax = 30000.00  # 30% of 100,000

        # Assert the calculated tax is correct
        self.assertEqual(tax, expected_tax)

        # Verify that the correct queries were executed
        self.mock_cursor.execute.assert_any_call("SELECT tax_rate FROM TaxTable WHERE employee_id = ?", (emp_id,))
        self.mock_cursor.execute.assert_any_call("INSERT INTO TaxRecords (employee_id, tax_amount) VALUES (?, ?)", (emp_id, expected_tax))

if __name__ == '__main__':
    unittest.main()
