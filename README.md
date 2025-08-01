# SENG8081-S25-Team5

# Project Contributors:
- Jyoti Maske
- Hiral Parekh
- Yash Khamar
- Neel Patel

# Project Title:
Online Retail Sales Analysis (E-Commerce)

# Project Objective:
Analyze customer purchase behavior, product popularity, and sales trends using a synthetic e-commerce dataset. This project simulates real-world online retail data to support data exploration, visualization, and predictive analytics.

# Data Sources
•	Kaggle Online Retail Dataset
•	(https://www.kaggle.com/datasets/carrie1/ecommerce-data) :
    It contains historical sales records with customer ID, invoice number, product codes, quantity, price, date, and location.
    Key Tables derived: Orders, OrderDetails, Customers, Products
•	FakeStoreAPI (https://fakestoreapi.com/products):
  It used to enrich products with additional metadata: Category, Brand, Rating, and ImageURL.
  This helps simulate a real-world catalog with diversified product types and associated attributes.
  
# Data Storage and Maintenance  
We are storing our data in SQL Server in below tables and cleaning using python libraries.
Brands
Customers
Orders
OrderDetails
Products

# Data Quality

To ensure high-quality and analysis-ready data, we performed the following:

- **Missing Value Handling**: Dropped rows missing essential fields (e.g., CustomerID, OrderID, ProductName, Quantity).
- **Data Type Standardization**: Converted columns like `OrderDate` to datetime format, and ensured numerical fields such as `UnitPrice` and `Rating` are floats.
- **Duplicate Removal**: Applied `.drop_duplicates()` to ensure unique entries in `Orders`, `Products`, and `Customers`.
- **Outlier Filtering**: Removed records with non-positive `Quantity` or `UnitPrice`.
- **Text Cleanup**: Trimmed whitespace and removed "Unspecified" or invalid values in country and brand fields.
- **Data Enrichment**: Filled in missing metadata such as Category, Brand, Rating, and ImageURL using the FakeStoreAPI or fallback logic.
- **Validation Rules**:
  - Rating must be between 0 and 5
  - Quantity and UnitPrice must be greater than 0
  - Referential integrity is ensured (e.g., every `CustomerID` in `Orders` exists in `Customers`)
    
# Data Visualization
The data visualization component of our E-Commerce Sales Analysis project is where all the efforts in data collection, cleaning, enrichment, and loading converge to produce actionable business insights. Using Tableau as our primary tool, we designed and implemented interactive dashboards and worksheets connected to our SQL Server database.

•	Tableau Desktop and Tableau Cloud: Used to build dynamic dashboards and data stories.
•	Live Connection to SQL Server: Ensures dashboards reflect the most recent data without auto and manual refreshes.

## Dashbords
Top Product Performance & Future Demand
Time & Territory Revenue Dashboard
Brand & Category Revenue Intelligence Dashboard
Product Volume and Order Distribution Across Brands
Top Product Ratings and Revenue Impact Segmentation

# Extensions

Real-Time Data Integration
•	Add live data streams using Kafka or Azure Event Hubs
•	Enables instant updates on orders, inventory, and customer activity
Predictive & Prescriptive Analytics
•	Use machine learning to forecast demand, churn, pricing, and recommendations
•	Moves from descriptive to smart decision-making
Customer Segmentation & Personalization
•	Apply RFM and clustering to group customers
•	Tailor offers and promotions for each segment
Multi-Channel Sales Analytics
•	Merge website, app, store, and social data
•	Helps analyze channel-wise performance and ROI
Cloud Migration & CI/CD
•	Shift ETL and database to cloud (AWS/Azure/GCP)
•	Add auto-deployment pipelines for scalability and efficiency






