import pyodbc
import math
from dao.loan_repository import ILoanRepository
from util.db_conn_util import get_db_connection
from exception.invalid_loan_exception import InvalidLoanException
from entity.customer import Customer
from entity.loan import Loan
from entity.home_loan import HomeLoan
from entity.car_loan import CarLoan

class LoanRepositoryImpl(ILoanRepository):

    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def apply_loan(self, loan: Loan):
        confirmation = input("Do you want to apply for the loan? (Yes/No): ").strip().lower()
        if confirmation != "yes":
            print("Loan application cancelled.")
            return

        try:
            loan_status = "Pending"

            insert_query = """
            INSERT INTO Loan (loan_id, customer_id, principal_amount, interest_rate, loan_term, loan_type, loan_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            self.cursor.execute(insert_query, (
                loan.loan_id,
                loan.customer.customer_id,
                loan.principal_amount,
                loan.interest_rate,
                loan.loan_term,
                loan.loan_type,
                loan_status
            ))

            if isinstance(loan, HomeLoan):
                home_query = "INSERT INTO HomeLoan (loan_id, property_address, property_value) VALUES (?, ?, ?)"
                self.cursor.execute(home_query, (
                    loan.loan_id,
                    loan.property_address,
                    loan.property_value
                ))

            elif isinstance(loan, CarLoan):
                car_query = "INSERT INTO CarLoan (loan_id, car_model, car_price) VALUES (?, ?, ?)"
                self.cursor.execute(car_query, (
                    loan.loan_id,
                    loan.car_model,
                    loan.car_price
                ))

            self.conn.commit()
            print("Loan application submitted successfully with status: Pending")

        except Exception as e:
            self.conn.rollback()
            print("Error while applying for loan:", e)

    def calculate_interest(self, loan_id):
        try:
            query = "SELECT principal_amount, interest_rate, loan_term FROM Loan WHERE loan_id = ?"
            self.cursor.execute(query, (loan_id,))
            result = self.cursor.fetchone()

            if result is None:
                raise InvalidLoanException(f"No loan found with ID: {loan_id}")

            principal, rate, term = result
            interest = (principal * rate * term) / 12
            print(f"Interest for Loan ID {loan_id} is: {interest}")
            return interest

        except InvalidLoanException as e:
            print(e)

    def calculate_interest_direct(self, principal_amount, interest_rate, loan_term):
        interest = (principal_amount * interest_rate * loan_term) / 12
        print(f"Calculated Interest: {interest}")
        return interest

    def loan_status(self, loan_id):
        try:
            loan_query = "SELECT customer_id FROM Loan WHERE loan_id = ?"
            self.cursor.execute(loan_query, (loan_id,))
            result = self.cursor.fetchone()

            if not result:
                raise InvalidLoanException(f"No loan found with ID: {loan_id}")

            customer_id = result[0]

            credit_query = "SELECT credit_score FROM Customer WHERE customer_id = ?"
            self.cursor.execute(credit_query, (customer_id,))
            credit_result = self.cursor.fetchone()

            if not credit_result:
                raise Exception(f"No customer found with ID: {customer_id}")

            credit_score = credit_result[0]
            status = "Approved" if credit_score > 650 else "Rejected"

            update_query = "UPDATE Loan SET loan_status = ? WHERE loan_id = ?"
            self.cursor.execute(update_query, (status, loan_id))
            self.conn.commit()

            print(f"Loan ID {loan_id} is {status} based on credit score {credit_score}")

        except InvalidLoanException as e:
            print(e)
        except Exception as ex:
            print("Error:", ex)

    def calculate_emi(self, loan_id):
        try:
            query = "SELECT principal_amount, interest_rate, loan_term FROM Loan WHERE loan_id = ?"
            self.cursor.execute(query, (loan_id,))
            result = self.cursor.fetchone()

            if result is None:
                raise InvalidLoanException(f"No loan found with ID: {loan_id}")

            principal, annual_rate, term_months = result
            monthly_rate = annual_rate / 12 / 100

            emi = (principal * monthly_rate * math.pow(1 + monthly_rate, term_months)) / \
                (math.pow(1 + monthly_rate, term_months) - 1)

            print(f"EMI for Loan ID {loan_id} is: {emi:.2f}")
            return emi

        except InvalidLoanException as e:
            print(e)

    def calculate_emi_direct(self, principal_amount, annual_rate, loan_term_months):
        monthly_rate = annual_rate / 12 / 100

        emi = (principal_amount * monthly_rate * math.pow(1 + monthly_rate, loan_term_months)) / \
            (math.pow(1 + monthly_rate, loan_term_months) - 1)

        print(f"Calculated EMI: {emi:.2f}")
        return emi

    def loan_repayment(self, loan_id, amount):
        try:
            query = "SELECT principal_amount, interest_rate, loan_term FROM Loan WHERE loan_id = ?"
            self.cursor.execute(query, (loan_id,))
            result = self.cursor.fetchone()

            if result is None:
                raise InvalidLoanException(f"No loan found with ID: {loan_id}")

            principal, annual_rate, loan_term = result
            monthly_rate = annual_rate / 12 / 100

            emi = (principal * monthly_rate * math.pow(1 + monthly_rate, loan_term)) / \
                (math.pow(1 + monthly_rate, loan_term) - 1)

            if amount < emi:
                print("Payment rejected: Amount is less than one EMI.")
            else:
                num_emis = int(amount // emi)
                print(f"Amount {amount} can pay {num_emis} full EMI(s) of {emi:.2f}")

        except InvalidLoanException as e:
            print(e)
        except Exception as ex:
            print("Error:", ex)

    def get_loan_by_id(self, loan_id):
        try:
            query = "SELECT * FROM Loan WHERE loan_id = ?"
            self.cursor.execute(query, (loan_id,))
            loan = self.cursor.fetchone()

            if loan is None:
                raise InvalidLoanException(f"No loan found with ID: {loan_id}")

            print("Loan Details:")
            print(loan)

        except InvalidLoanException as e:
            print(e)
        except Exception as e:
            print("Error retrieving loan by ID:", e)

    def calculate_emi_params(self, principal, rate, term):
        monthly_rate = rate / 12 / 100
        emi = (principal * monthly_rate * math.pow(1 + monthly_rate, term)) / \
              (math.pow(1 + monthly_rate, term) - 1)
        return emi

    def calculate_interest_params(self, principal, rate, term):
        interest = (principal * rate * term) / 12
        return interest

    def get_all_loans(self):
        try:
            query = "SELECT * FROM Loan"
            self.cursor.execute(query)
            loans = self.cursor.fetchall()
            for loan in loans:
                print(loan)
        except Exception as e:
            print("Error fetching all loans:", e)
