
-- Update for CustomerID = 1
UPDATE customers_t
SET email = 'johndoe@gmail.com'
WHERE customerid = 1;

-- Update for CustomerID = 2
UPDATE customers_t
SET phone = '555-5679'
WHERE customerid = 2;

-- Update for CustomerID = 3
UPDATE customers_t
SET address = '123 Elm Ln',
    city = 'Harborcity',
    state = 'FL',
    zipcode = 87654
WHERE customerid = 3;

-- Insert for CustomerID = 11
INSERT INTO customers_t (customerid, firstname, lastname, email, phone, address, city, state, zipcode)
VALUES (11, 'Grace', 'Turner', 'graceturner@email.com', '555-1122', '567 Oak St', 'Cityview', 'CA', 98765);

-- Insert for CustomerID = 12
INSERT INTO customers_t (customerid, firstname, lastname, email, phone, address, city, state, zipcode)
VALUES (12, 'Connor', 'Evans', 'connorevans@email.com', '555-2233', '890 Pine Ave', 'T ownsville', 'TX', 54321);

-- Delete for CustomerID = 10
DELETE FROM customers_t
WHERE customerid = 10;

SELECT * FROM customers_t ORDER BY customerid;
