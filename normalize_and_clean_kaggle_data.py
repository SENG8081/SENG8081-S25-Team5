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

# Remove unwanted countries
kaggle_data = kaggle_data[~kaggle_data["Country"].isin(["Unspecified", "European Community"])]

# --------------------------
# STEP 2: Normalize Tables
# --------------------------

# Orders Table
orders = kaggle_data[["InvoiceNo", "InvoiceDate", "CustomerID"]].drop_duplicates()
orders.columns = ["OrderID", "OrderDate", "CustomerID"]
orders["OrderDate"] = pd.to_datetime(orders["OrderDate"], errors="coerce")

def random_date(start_year=2020):
    start = pd.Timestamp(f"{start_year}-01-01")
    end = pd.Timestamp.today()
    return start + pd.to_timedelta(np.random.randint(0, (end - start).days), unit='D')

orders["OrderDate"] = [random_date() for _ in range(len(orders))]
orders = orders.dropna(subset=["OrderID", "OrderDate", "CustomerID"]).drop_duplicates(subset=["OrderID"])

# OrderDetails Table
order_details = kaggle_data[["InvoiceNo", "StockCode", "Quantity", "UnitPrice"]]
order_details.columns = ["OrderID", "ProductID", "Quantity", "UnitPrice"]
order_details = order_details[(order_details["Quantity"] > 0) & (order_details["UnitPrice"] > 0)].drop_duplicates()

# Customers Table
customers = kaggle_data[["CustomerID", "Country"]].drop_duplicates()
customers = customers.drop_duplicates(subset=["CustomerID"])
customers = customers.dropna(subset=["CustomerID", "Country"])
customers["Country"] = customers["Country"].str.strip()
customers = customers[~customers["Country"].isin(["Unspecified", "European Community"])]

# Products Table (Initial)
products = kaggle_data[["StockCode", "Description"]].dropna()
products.columns = ["ProductID", "ProductName"]
products = products[products["ProductName"].str.strip() != ""].drop_duplicates(subset=["ProductID"])

# --------------------------
# STEP 3: Enrich Products with FakeStoreAPI
# --------------------------
try:
    response = requests.get("https://fakestoreapi.com/products?limit=150")
    response.raise_for_status()
    api_data = response.json()

    brand_dict = {
        "Electronics": ["Apple", "Samsung", "Sony", "Dell"],
        "Jewelery": ["Tiffany", "Swarovski", "Cartier"],
        "Men's Clothing": ["Zara", "H&M", "Nike"],
        "Women's Clothing": ["Gucci", "Chanel", "Prada"]
    }

    def standardize_category(cat):
        mapping = {
            "electronics": "Electronics",
            "jewelery": "Jewelery",
            "men's clothing": "Men's Clothing",
            "women's clothing": "Women's Clothing"
        }
        return mapping.get(cat.strip().lower(), cat.title())

    api_df = pd.DataFrame([{
        "API_ProductName": p["title"],
        "Category": standardize_category(p["category"]),
        "BrandName": random.choice(brand_dict.get(standardize_category(p["category"]), ["GenericBrand"])),
        "Rating": p["rating"]["rate"],
        "ImageURL": p["image"]
    } for p in api_data])

    # Sample to match number of products
    api_sample = api_df.sample(n=len(products), replace=True).reset_index(drop=True)
    products = products.reset_index(drop=True)

    products["ProductName"] = api_sample["API_ProductName"]
    products["Category"] = api_sample["Category"]
    products["BrandName"] = api_sample["BrandName"]
    products["Rating"] = api_sample["Rating"]
    products["ImageURL"] = api_sample["ImageURL"]

except Exception:
    print("Failed to fetch from API. Using fallback enrichment.")
    categories = ["electronics", "books", "home decor", "fashion", "fitness"]
    products["Category"] = np.random.choice(categories, size=len(products))
    products["BrandName"] = products["Category"]  # fallback
    products["Rating"] = np.random.uniform(3.0, 5.0, size=len(products)).round(1)
    products["ImageURL"] = "https://via.placeholder.com/150"

# --------------------------
# STEP 4: Generate Brands Table with BrandID and Category
# --------------------------
brands = products[["BrandName", "Category"]].drop_duplicates().reset_index(drop=True)
brands["BrandID"] = brands.index + 1  # simulate sequential BrandID

# Final products table as per schema
final_products = products[["ProductID", "ProductName", "Category", "BrandName", "Rating", "ImageURL"]]

# --------------------------
# STEP 5: Save Cleaned + Enriched Tables
# --------------------------
orders.to_csv("C:\\Users\\jyoro\\Downloads\\clean_orders.csv", index=False)
order_details.to_csv("C:\\Users\\jyoro\\Downloads\\clean_order_details.csv", index=False)
customers.to_csv("C:\\Users\\jyoro\\Downloads\\clean_customers.csv", index=False)
final_products.to_csv("C:\\Users\\jyoro\\Downloads\\clean_products.csv", index=False)
brands[["BrandID", "BrandName", "Category"]].to_csv("C:\\Users\\jyoro\\Downloads\\clean_brands.csv", index=False)

print("All cleaned and enriched tables saved as CSV.")
