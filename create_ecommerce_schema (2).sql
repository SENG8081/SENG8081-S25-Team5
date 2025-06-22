-- SQL Server Script: Create Tables for E-Commerce Project

-- Drop tables if they exist to avoid conflicts
IF OBJECT_ID('OrderDetails', 'U') IS NOT NULL DROP TABLE OrderDetails;
IF OBJECT_ID('Orders', 'U') IS NOT NULL DROP TABLE Orders;
IF OBJECT_ID('Products', 'U') IS NOT NULL DROP TABLE Products;
IF OBJECT_ID('Customers', 'U') IS NOT NULL DROP TABLE Customers;
IF OBJECT_ID('Brands', 'U') IS NOT NULL DROP TABLE Brands;

-- Create Brands Table
CREATE TABLE Brands (
    BrandID INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incremented primary key
    BrandName VARCHAR(255) NOT NULL UNIQUE  -- Brand name must be unique
);

-- Create Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Country VARCHAR(100)
);

-- Create Products Table
CREATE TABLE Products (
    ProductID VARCHAR(50) PRIMARY KEY,
    ProductName VARCHAR(255),
    Category VARCHAR(100),
    Brand VARCHAR(255),
    Rating FLOAT,
    ImageURL VARCHAR(500),
    FOREIGN KEY (Brand) REFERENCES Brands(BrandName)
);

-- Create Orders Table
CREATE TABLE Orders (
    OrderID VARCHAR(50) PRIMARY KEY,
    OrderDate DATETIME,
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Create OrderDetails Table
CREATE TABLE OrderDetails (
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID VARCHAR(50),
    ProductID VARCHAR(50),
    Quantity INT,
    UnitPrice FLOAT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

select * from Brands;
select * from Customers;
select * from OrderDetails;
select * from Orders;
select * from Products;