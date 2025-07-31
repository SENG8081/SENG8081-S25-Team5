import pandas as pd
import time
import pyodbc

BATCH_SIZE = 10
POLL_INTERVAL = 2  
MAX_BATCHES = 10   

# -------------------------- CONNECT TO DB --------------------------
def connect_to_db():
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=NEEL;'
                              'DATABASE=Sales_Analysis;'
                              'UID=sa;'
                              'PWD=Neel8971512;')
        print(" Connected to SQL Server.")
        return conn
    except pyodbc.Error as e:
        print(" Database connection failed:", e)
        return None

# -------------------------- INSERT FUNCTION --------------------------
def insert_batch(cursor, batch):
    for _, row in batch.iterrows():
        try:
            cursor.execute("""
                INSERT INTO Products (ProductID, ProductName, Category, Brand, Rating, ImageURL)
                VALUES (?, ?, ?, ?, ?, ?)""",
                row["ProductID"], row["ProductName"], row["Category"], row["BrandName"],
                float(row["Rating"]), row["ImageURL"])
        except Exception as e:
            print(" Error inserting record:", row["ProductID"], e)

# -------------------------- SIMULATION --------------------------
def simulate_batch_stream():
    # Read product data from CSV
    products = pd.read_csv("D:\\BigData\\Semester 2\\Case Studies\\Project\\clean_products.csv")
    products = products.sample(frac=1).reset_index(drop=True) 

    conn = connect_to_db()
    if conn is None:
        return

    cursor = conn.cursor()
    total = len(products)
    pointer = 0
    batch_num = 1

    while pointer < total and batch_num <= MAX_BATCHES:
        batch = products.iloc[pointer: pointer + BATCH_SIZE]
        print(f"Sending Batch {batch_num} with {len(batch)} records")
        insert_batch(cursor, batch)
        conn.commit()
        print(f" Batch {batch_num} committed.\n")
        pointer += BATCH_SIZE
        batch_num += 1
        time.sleep(POLL_INTERVAL)

    cursor.close()
    conn.close()
    print(" Real-time simulation complete.")

# -------------------------- RUN --------------------------
if __name__ == "__main__":
    simulate_batch_stream()

