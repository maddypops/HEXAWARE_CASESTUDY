from abc import ABC, abstractmethod


class IFinancialRecordService(ABC):

    @abstractmethod
    def add_financial_record(self, employee_id, description, amount, record_type, record_date):
        pass

    @abstractmethod
    def get_financial_record_by_id(self, record_id):
        pass

    @abstractmethod
    def get_financial_records_for_employee(self, employee_id):
        pass

    @abstractmethod
    def get_financial_records_for_date(self, record_date):
        pass
