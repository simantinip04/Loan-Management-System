from util.db_conn_util import get_db_connection
from entity.customer import Customer

class CustomerDAOImpl:
    def add_customer(self, customer: Customer):
        conn = get_db_connection()
        if conn is None:
            print("❌ Could not connect to the database.")
            return
        
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO Customer (customer_id, name, credit_score)
                VALUES (?, ?, ?)
            '''
            cursor.execute(query, customer.customer_id, customer.name, customer.credit_score)
            conn.commit()
            print("✅ Customer added successfully.")
        except Exception as e:
            print("❌ Error while adding customer:", e)
        finally:
            conn.close()

    def customer_exists(self, cust_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Customer WHERE customer_id = ?", (cust_id,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print("❌ Error checking customer existence:", e)
            return False
        finally:
            if conn:
                conn.close()
