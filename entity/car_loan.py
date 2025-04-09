from entity.loan import Loan

class CarLoan(Loan):
    def __init__(self, loan_id, customer, principal_amount, interest_rate, loan_term, car_model, car_price):
        super().__init__(loan_id, customer, principal_amount, interest_rate, loan_term, "Car")
        self.car_model = car_model
        self.car_price = car_price



    def _str_(self):
        return super()._str_() + f", Car Model: {self.car_model}, Car Value: {self.car_price}"