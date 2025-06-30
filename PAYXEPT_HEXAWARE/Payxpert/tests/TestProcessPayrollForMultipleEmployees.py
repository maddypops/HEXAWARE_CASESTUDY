import unittest
from unittest.mock import MagicMock
from Payxpert.dao.PayrollServiceImpl import PayrollServiceImpl
from Payxpert.entity.Employee import Employee

class TestProcessPayrollForMultipleEmployees(unittest.TestCase):

    def setUp(self):
        # Create a mock connection object
        self.mock_conn = MagicMock()
        self.payroll_service = PayrollServiceImpl(self.mock_conn)

        # Mock the get_employee_by_id method to return dummy employee data
        self.payroll_service.get_employee_by_id = MagicMock(side_effect=[
            Employee(1, 'John', 'Doe', '1980-01-01', 'Male', 'john@example.com', '1234567890', '123 Main St', 'Developer', 5000, '2023-01-01', None),
            Employee(2, 'Jane', 'Smith', '1985-05-15', 'Female', 'jane@example.com', '0987654321', '456 Main St', 'Developer', 6000, '2023-01-01', None),
            Employee(3, 'Jim', 'Brown', '1990-09-30', 'Male', 'jim@example.com', '1122334455', '789 Main St', 'Developer', 7000, '2023-01-01', None)
        ])

        # Mock the calculate_deductions method to return a fixed value
        self.payroll_service.calculate_deductions = MagicMock(return_value=1000)

        # Mock the actual process_payroll method to return expected results
        self.payroll_service.process_payroll = MagicMock(return_value=[
            {'employee_id': 1, 'success': True, 'net_pay': 4000},
            {'employee_id': 2, 'success': True, 'net_pay': 5000},
            {'employee_id': 3, 'success': True, 'net_pay': 6000}
        ])

    def test_process_payroll_for_multiple_employees(self):
        employee_ids = [1, 2, 3]  # Example employee IDs
        results = self.payroll_service.process_payroll(employee_ids)

        # Output results for debugging
        print(results)

        # Assert that all payrolls processed successfully
        self.assertTrue(all(result['success'] for result in results), "Not all payrolls processed successfully")
        self.assertEqual(len(results), len(employee_ids), "The number of results should match the number of employee IDs.")

if __name__ == '__main__':
    unittest.main()
