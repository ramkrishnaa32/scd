
DROP TABLE IF EXISTS customers_t;

CREATE TABLE customers_t (
    customerid BIGINT PRIMARY KEY,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zipcode BIGINT
);

INSERT INTO customers_t (customerid, firstname, lastname, email, phone, address, city, state, zipcode) VALUES
(1, 'John', 'Doe', 'johndoe@email.com', '555-1234', '123 Main St', 'Anytown', 'CA', 12345),
(2, 'Jane', 'Smith', 'janesmith@email.com', '555-5678', '456 Oak Ave', 'Sometown', 'NY', 67890),
(3, 'Robert', 'Johnson', 'robertjohnson@email.com', '555-8765', '789 Pine Ln', 'Othercity', 'TX', 34567),
(4, 'Alice', 'Williams', 'alicewilliams@email.com', '555-4321', '234 Cedar Dr', 'Yourtown', 'FL', 89012),
(5, 'Michael', 'Brown', 'michaelbrown@email.com', '555-9876', '567 Elm Blvd', 'Theirtown', 'IL', 45678),
(6, 'Emily', 'Miller', 'emilymiller@email.com', '555-6543', '890 Birch Rd', 'Newcity', 'WA', 23456),
(7, 'David', 'Jones', 'davidjones@email.com', '555-2345', '678 Maple Ave', 'Yourcity', 'GA', 78901),
(8, 'Sarah', 'Anderson', 'sarahanderson@email.com', '555-5432', '901 Pine St', 'Heretown', 'OH', 56789),
(9, 'Christopher', 'Taylor', 'christophertaylor@email.com', '555-8765', '234 Oak Ln', 'Thistown', 'PA', 12345),
(10, 'Olivia', 'Clark', 'oliviaclark@email.com', '555-3456', '567 Cedar Ave', 'Thatcity', 'TN', 67890);

SELECT * FROM customers_t ORDER BY customerid;

DROP TABLE IF EXISTS customers_scd;
CREATE TABLE customers_scd (
    customerid BIGINT,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zipcode BIGINT,
    customer_skey BIGINT,
    effective_date DATE,
    end_date DATE,
    active_flag BOOLEAN
);

SELECT * FROM customers_scd ORDER BY customerid;

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
