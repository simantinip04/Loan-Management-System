import pyodbc
from entity.loan import Loan
from entity.home_loan import HomeLoan
from entity.car_loan import CarLoan
from util.db_conn_util import get_db_connection

class LoanDAOImpl:
    def apply_loan(self, loan):
        conn = get_db_connection()
        if conn is None:
            print("❌ Could not connect to the database.")
            return

        try:
            cursor = conn.cursor()

            # Insert into Loan table
            cursor.execute("""
                INSERT INTO Loan (loan_id, customer_id, principal_amount, interest_rate, loan_term, loan_type, loan_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                loan.loan_id,
                loan.customer.customer_id,
                loan.principal_amount,
                loan.interest_rate,
                loan.loan_term,
                loan.loan_type,
                "Active"
            ))

            # Insert into subtype table
            if isinstance(loan, HomeLoan):
                cursor.execute("""
                    INSERT INTO HomeLoan (loan_id, property_address, property_value)
                    VALUES (?, ?, ?)
                """, (
                    loan.loan_id,
                    loan.property_address,
                    loan.property_value
                ))
            elif isinstance(loan, CarLoan):
                cursor.execute("""
                    INSERT INTO CarLoan (loan_id, car_model, car_price)
                    VALUES (?, ?, ?)
                """, (
                    loan.loan_id,
                    loan.car_model,
                    loan.car_price
                ))

            conn.commit()
            print("✅ Loan applied successfully.")
        except Exception as e:
            print("❌ Error while applying for loan:", e)
        finally:
            conn.close()

    def get_loan_by_id(self, loan_id):
        conn = get_db_connection()
        if conn is None:
            print("❌ Could not connect to the database.")
            return

        try:
            cursor = conn.cursor()

            # Fetch loan from Loan table
            cursor.execute("SELECT loan_id, customer_id, amount, interest_rate, loan_term, loan_type, loan_status FROM Loan WHERE loan_id = ?", (loan_id,))
            loan = cursor.fetchone()

            if loan:
                print("\n✅ Loan Found:")
                print(f"Loan ID       : {loan.loan_id}")
                print(f"Customer ID   : {loan.customer_id}")
                print(f"Amount        : {loan.principal_amount}")
                print(f"Interest Rate : {loan.interest_rate}")
                print(f"Term          : {loan.loan_term} months")
                print(f"Loan Type     : {loan.loan_type}")
                print(f"Status        : {loan.loan_status}")

                # Optional: You can also fetch subtype info based on loan_type
                if loan.loan_type == "Home":
                    cursor.execute("SELECT property_address, property_value FROM HomeLoan WHERE loan_id = ?", (loan_id,))
                    home_loan = cursor.fetchone()
                    if home_loan:
                        print(f"Property Location : {home_loan.property_address}")
                        print(f"Property Value    : {home_loan.property_value}")
                elif loan.loan_type == "Car":
                    cursor.execute("SELECT car_model, car_price FROM CarLoan WHERE loan_id = ?", (loan_id,))
                    car_loan = cursor.fetchone()
                    if car_loan:
                        print(f"Car Model  : {car_loan.car_model}")
                        print(f"Car Price  : {car_loan.car_price}")
            else:
                print("❌ No loan found with the given ID.")

            cursor.close()
        except Exception as e:
            print("❌ Error while fetching loan details:", e)
        finally:
            conn.close()
