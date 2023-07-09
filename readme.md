# Project Name

This is a sample project that demonstrates the usage of FastAPI and SQLAlchemy for building a RESTful API.

## Description

The project provides endpoints for managing products and orders. It utilizes FastAPI as the web framework, SQLAlchemy as the ORM for interacting with the database, and PostgreSQL as the database backend.
## Installation
 Clone the repository
All the dependencies are in the project (venv file)

Set up the database:

   1. Make sure you have PostgreSQL installed and running.
   2. Update the DATABASE_URL variable in main.py with your PostgreSQL connection details.

## Usage

    Start the server:

    uvicorn main:app --reload

    Open your web browser and navigate to http://localhost:8000/docs to access the Swagger UI documentation and interact with the API.

    Use the provided endpoints to manage products and orders. You can view, create, update, and delete products and orders using the API.

API Endpoints

    GET /products: Retrieve all products.
    POST /orders: Create a new order.
    GET /orders: Retrieve a list of orders with pagination support.
    GET /orders/{order_id}: Retrieve a specific order by ID.
    PUT /products/{product_id}: Update the quantity of a product.
    


