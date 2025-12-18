CREATE TABLE IF NOT EXISTS author (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS book (
    id INT PRIMARY KEY,
    title VARCHAR(100),
    author_id INT,
    qty INT,
    FOREIGN KEY (author_id) REFERENCES author(id)
);