import numpy as np
import pandas as pd
import pyodbc

# --------------------------
# STEP 1: Connect to SQL Server
# --------------------------
def connect_to_db():
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                            'SERVER=Jyoti\\SQLEXPRESS;'
                            'DATABASE=Sales_Analysis;'
                            'Trusted_Connection=yes;')
        return conn
    except pyodbc.Error as e:
        print("Database connection failed:", e)
        return None

# --------------------------
# STEP 2: Load CSV Data
# --------------------------
brands = pd.read_csv("C:\\Users\\jyoro\\Downloads\\clean_brands.csv")
customers = pd.read_csv("C:\\Users\\jyoro\\Downloads\\clean_customers.csv")
products = pd.read_csv("C:\\Users\\jyoro\\Downloads\\clean_products.csv")  # uses 'Brand' column
orders = pd.read_csv("C:\\Users\\jyoro\\Downloads\\clean_orders.csv")
order_details = pd.read_csv("C:\\Users\\jyoro\\Downloads\\clean_order_details.csv")

# --------------------------
# STEP 3: Insert Data into SQL Server
# --------------------------
def insert_all_data():
    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()

    # DELETE from child to parent to avoid FK conflicts
    try:
        cursor.execute("DELETE FROM OrderDetails")
        cursor.execute("DELETE FROM Orders")
        cursor.execute("DELETE FROM Products")
        cursor.execute("DELETE FROM Customers")
        cursor.execute("DELETE FROM Brands")
        cursor.execute("DBCC CHECKIDENT ('Brands', RESEED, 0);")
        conn.commit()
    except Exception as e:
        print("Error during deletion:", e)


    # Insert unique brands first and build mapping of BrandName -> BrandID
    brand_ids = {}
    for _, row in brands.iterrows():
        brand_name = str(row["BrandName"]).strip()
        category = str(row["Category"]).strip()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM Brands WHERE BrandName = ? AND Category = ?)
                INSERT INTO Brands (BrandName, Category) VALUES (?, ?)
            """, brand_name, category, brand_name, category)
        except Exception as e:
            print("Error inserting brand:", brand_name, e)

    # Commit so we can fetch BrandIDs
    conn.commit()

    # Fetch all brand IDs
    cursor.execute("SELECT BrandID, BrandName FROM Brands")
    for row in cursor.fetchall():
        brand_ids[row.BrandName.strip()] = row.BrandID

    # Insert into Products table
    for _, row in products.iterrows():
        brand_name = str(row['BrandName']).strip()
        brand_id = brand_ids.get(brand_name, None)

        # Clean rating
        try:
            rating = float(row['Rating'])
        except:
            rating = 0.0

        try:
            cursor.execute("""
                INSERT INTO Products (ProductID, ProductName, Category, Brand, Rating, ImageURL)
                VALUES (?, ?, ?, ?, ?, ?)
            """, row['ProductID'], row['ProductName'], row['Category'], brand_name, rating, row['ImageURL'])
        except Exception as e:
            print("Error inserting product:", row['ProductID'], e)

    # Insert customers
    for _, row in customers.iterrows():
        cursor.execute("INSERT INTO Customers (CustomerID, Country) VALUES (?, ?)",
                    int(row["CustomerID"]), row["Country"])

    # Insert orders
    
    for _, row in orders.iterrows():
        cursor.execute("INSERT INTO Orders (OrderID, OrderDate, CustomerID) VALUES (?, ?, ?)",
                    row["OrderID"], row["OrderDate"], int(row["CustomerID"]))

    # Insert order details
    for _, row in order_details.iterrows():
        cursor.execute("""
            INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice)
            VALUES (?, ?, ?, ?)""",
            row["OrderID"], row["ProductID"], int(row["Quantity"]), float(row["UnitPrice"]))

    conn.commit()
    cursor.close()
    conn.close()
    print("All tables loaded into SQL Server successfully.")

if __name__ == "__main__":
    insert_all_data()
