import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Database connection parameters
db_params = {
    "host": "localhost",
    "database": "test",
    "user": "postgres",
    "password": "A123654789B"
}

fake = Faker()

# Function to insert dummy data into tables
def insert_data(conn):
    cur = conn.cursor()

    # Insert customer data
    for _ in range(100):
        customer_name = fake.name()
        customer_address = fake.address().replace('\n', ', ')
        customer_phone = fake.phone_number()[:20]
        print(len(customer_phone))
        customer_email = fake.email()

        cur.execute("""
            INSERT INTO public.customer (customer_name, customer_address, customer_phone, customer_email)
            VALUES (%s, %s, %s, %s)
        """, (customer_name, customer_address, customer_phone, customer_email))

    # Insert product data
    for _ in range(50):
        product_name = fake.bs()
        product_description = fake.catch_phrase()
        unit_price = round(random.uniform(1, 100), 2)

        cur.execute("""
            INSERT INTO public.product (product_name, product_description, unit_price)
            VALUES (%s, %s, %s)
        """, (product_name, product_description, unit_price))

    # Insert shipment and invoice data
    for customer_id in range(1, 101):
        shipment_date = fake.date_between(start_date='-3y', end_date='today')
        source_location = fake.city()
        destination_location = fake.city()
        shipment_type = random.choice(['Express', 'Standard', 'Economy'])
        shipment_status = random.choice(['Shipped', 'In Transit', 'Delivered', 'Cancelled'])

        cur.execute("""
            INSERT INTO public.shipment (customer_id, shipment_date, source_location, destination_location, shipment_type, shipment_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING shipment_id
        """, (customer_id, shipment_date, source_location, destination_location, shipment_type, shipment_status))
        
        shipment_id = cur.fetchone()[0]

        invoice_date = shipment_date
        due_date = invoice_date + timedelta(days=30)
        total_amount_due = round(random.uniform(50, 1000), 2)

        cur.execute("""
            INSERT INTO public.invoice (customer_id, shipment_id, invoice_date, due_date, total_amount_due)
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_id, shipment_id, invoice_date, due_date, total_amount_due))

    # Insert payment data
    for invoice_id in range(1, 101):
        payment_date = fake.date_between(start_date='-3y', end_date='today')
        payment_method = random.choice(['Credit Card', 'Debit Card', 'Bank Transfer', 'Cash'])
        amount_paid = round(random.uniform(1, 100), 2)

        cur.execute("""
            INSERT INTO public.payment (invoice_id, payment_date, payment_method, amount_paid)
            VALUES (%s, %s, %s, %s)
        """, (invoice_id, payment_date, payment_method, amount_paid))

    conn.commit()

# Main function to connect to the database and insert dummy data
def main():
    with psycopg2.connect(**db_params) as conn:
        insert_data(conn)

if __name__ == '__main__':
    main()