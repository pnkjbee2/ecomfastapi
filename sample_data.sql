--
-- PostgreSQL database dump
--
-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    price FLOAT NOT NULL,
    quantity INTEGER NOT NULL
);

-- Create the orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    timestamp VARCHAR DEFAULT CURRENT_TIMESTAMP,
    total_amount FLOAT NOT NULL,
    user_address_city VARCHAR NOT NULL,
    user_address_country VARCHAR NOT NULL,
    user_address_zip_code VARCHAR NOT NULL
);

-- Create the order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER NOT NULL,
    bought_quantity INTEGER NOT NULL
);

-- Insert sample data into the products table
INSERT INTO products (name, price, quantity)
VALUES ('Product 1', 10.99, 20),
       ('Product 2', 5.99, 15),
       ('Product 3', 7.99, 30);

-- Insert sample data into the orders table
INSERT INTO orders (timestamp, total_amount, user_address_city, user_address_country, user_address_zip_code)
VALUES (CURRENT_TIMESTAMP, 25.98, 'City A', 'Country X', '12345'),
       (CURRENT_TIMESTAMP, 18.97, 'City B', 'Country Y', '54321');

-- Insert sample data into the order_items table
INSERT INTO order_items (order_id, product_id, bought_quantity)
VALUES (1, 1, 2),
       (1, 2, 3),
       (2, 2, 1),
       (2, 3, 2);

-- Set the sequence values for auto-incrementing columns
SELECT SETVAL('products_id_seq', COALESCE((SELECT MAX(id) + 1 FROM products), 1), false);
SELECT SETVAL('orders_id_seq', COALESCE((SELECT MAX(id) + 1 FROM orders), 1), false);
SELECT SETVAL('order_items_id_seq', COALESCE((SELECT MAX(id) + 1 FROM order_items), 1), false);
