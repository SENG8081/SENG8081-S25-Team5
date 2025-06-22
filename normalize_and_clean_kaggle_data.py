import pandas as pd
import numpy as np
import requests
import random

# --------------------------
# STEP 1: Read Kaggle Flat File
# --------------------------
kaggle_data = pd.read_csv("C:\\Users\\jyoro\\Downloads\\data.csv", encoding="ISO-8859-1")

# Drop missing important values
kaggle_data = kaggle_data.dropna(subset=["CustomerID", "Description", "InvoiceNo", "InvoiceDate", "StockCode", "Quantity", "UnitPrice"])

# --------------------------
# STEP 2: Normalize Tables from Flat File
# --------------------------
# Orders Table
orders = kaggle_data[["InvoiceNo", "InvoiceDate", "CustomerID"]].drop_duplicates()
orders.columns = ["OrderID", "OrderDate", "CustomerID"]
orders["OrderDate"] = pd.to_datetime(orders["OrderDate"], errors="coerce")
orders = orders.dropna(subset=["OrderID", "OrderDate", "CustomerID"])
orders = orders.drop_duplicates(subset=["OrderID"])

# OrderDetails Table
order_details = kaggle_data[["InvoiceNo", "StockCode", "Quantity", "UnitPrice"]]
order_details.columns = ["OrderID", "ProductID", "Quantity", "UnitPrice"]
order_details = order_details[(order_details["Quantity"] > 0) & (order_details["UnitPrice"] > 0)]
order_details = order_details.drop_duplicates()

# Customers Table
customers = kaggle_data[["CustomerID", "Country"]].drop_duplicates()
customers = customers.dropna()
customers = customers.drop_duplicates(subset=["CustomerID"])

# Products Table
products = kaggle_data[["StockCode", "Description"]].dropna()
products.columns = ["ProductID", "ProductName"]
products = products[products["ProductName"].str.strip() != ""]
products = products.drop_duplicates(subset=["ProductID"])

# --------------------------
# STEP 4: Enrich Products from FakeStoreAPI (if online)
# --------------------------
try:
    response = requests.get("https://fakestoreapi.com/products")
    response.raise_for_status()
    api_data = response.json()

    # Create dataframe with unique names to avoid ProductName conflict
    api_df = pd.DataFrame([{
        "API_ProductName": p["title"],
        "Category": p["category"],
        "Brand": p["category"],
        "Rating": p["rating"]["rate"],
        "ImageURL": p["image"]
    } for p in api_data])


    # If less API rows than product rows, sample with replacement
    api_sample = api_df.sample(n=len(products), replace=True).reset_index(drop=True)
    products = products.reset_index(drop=True)

    products["ProductName"] = api_sample["API_ProductName"]
    products["Category"] = api_sample["Category"]
    products["Brand"] = api_sample["Brand"]
    products["Rating"] = api_sample["Rating"]
    products["ImageURL"] = api_sample["ImageURL"]

    enriched_products = products  # now complete with new columns

except Exception:
    print(" Failed to fetch from API. Using random enrichment instead.")
    categories = ["electronics", "books", "home decor", "fashion", "fitness"]
    enriched_products = products.copy()
    enriched_products["Category"] = np.random.choice(categories, size=len(products))
    enriched_products["Brand"] = enriched_products["Category"]
    enriched_products["Rating"] = np.random.uniform(3.0, 5.0, size=len(products)).round(1)
    enriched_products["ImageURL"] = "https://via.placeholder.com/150"

brands = enriched_products["Brand"].drop_duplicates().to_frame(name="BrandName")

# --------------------------
# STEP 5: Save Cleaned + Enriched Tables as CSV
# --------------------------
orders.to_csv("C:\\Users\\jyoro\\Downloads\\clean_orders.csv", index=False)
order_details.to_csv("C:\\Users\\jyoro\\Downloads\\clean_order_details.csv", index=False)
customers.to_csv("C:\\Users\\jyoro\\Downloads\\clean_customers.csv", index=False)
enriched_products.to_csv("C:\\Users\\jyoro\\Downloads\\clean_products.csv", index=False)
brands.to_csv("C:\\Users\\jyoro\\Downloads\\clean_brands.csv", index=False)

print("All cleaned tables saved as CSV.")
