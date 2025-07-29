-- Drop tables if they exist
IF OBJECT_ID('OrderDetails', 'U') IS NOT NULL DROP TABLE OrderDetails;
IF OBJECT_ID('Orders', 'U') IS NOT NULL DROP TABLE Orders;
IF OBJECT_ID('Products', 'U') IS NOT NULL DROP TABLE Products;
IF OBJECT_ID('Customers', 'U') IS NOT NULL DROP TABLE Customers;
IF OBJECT_ID('Brands', 'U') IS NOT NULL DROP TABLE Brands;

-- Brands Table
CREATE TABLE Brands (
    BrandID INT IDENTITY(1,1) PRIMARY KEY,
    BrandName VARCHAR(255) NOT NULL UNIQUE,
    Category VARCHAR(100) NOT NULL
);

-- Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Country VARCHAR(100)
);

-- Products Table
CREATE TABLE Products (
    ProductID VARCHAR(50) PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    Category VARCHAR(100) NOT NULL,
    Brand VARCHAR(255) NOT NULL,
    Rating FLOAT CHECK (Rating BETWEEN 1 AND 5),
    ImageURL VARCHAR(500),
    FOREIGN KEY (Brand) REFERENCES Brands(BrandName)
);

-- Orders Table
CREATE TABLE Orders (
    OrderID VARCHAR(50) PRIMARY KEY,
    OrderDate DATETIME NOT NULL,
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- OrderDetails Table
CREATE TABLE OrderDetails (
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID VARCHAR(50),
    ProductID VARCHAR(50),
    Quantity INT CHECK (Quantity > 0),
    UnitPrice FLOAT CHECK (UnitPrice >= 0),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);


