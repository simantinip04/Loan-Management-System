import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from entity.loan import Loan

class HomeLoan(Loan):
    def __init__(self, loan_id=0, customer=None, principal_amount=0.0, interest_rate=0.0,
                 loan_term=0, loan_status="Pending", property_address="", property_value=0):
        super()._init_(loan_id, customer, principal_amount, interest_rate, loan_term, "HomeLoan", loan_status)
        self.property_address = property_address
        self.property_value = property_value

    def __str__(self):
        return super().__str__() + f", Property Address: {self.property_address}, Property Value: {self.property_value}"