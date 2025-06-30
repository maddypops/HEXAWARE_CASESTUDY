import unittest
from Payxpert.dao.PayrollServiceImpl import PayrollServiceImpl


class TestCalculateNetSalaryAfterDeductions(unittest.TestCase):

    def setUp(self):
        self.payroll_service = PayrollServiceImpl(None)  # Mocking database connection

    def test_calculate_net_salary_after_deductions(self):
        gross_salary = 5000.00
        deductions = 1000.00  # Example deduction
        net_salary = self.payroll_service.calculate_net_salary(gross_salary, deductions)

        # Print the calculated net salary for verification
        print(f"Calculated Net Salary: {net_salary}")

        expected_net_salary = 4000.00  # Modify as per your logic
        self.assertEqual(net_salary, expected_net_salary)


if __name__ == '__main__':
    unittest.main()
