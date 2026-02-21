# Inventory_Management_System
Python / SQL Database Bookstore management program. Capstone Project.

This project is a Python-based inventory management system backed by a SQL database, designed to manage bookstore inventory efficiently and securely. The application supports full CRUD (Create, Read, Update, Delete) operations through a menu-driven interface and emphasizes secure database interaction using Prepared Statements to mitigate SQL Injection (SQLi) risks.


Security-Focused Design

All database operations in this project are implemented using SQL prepared statments (parameterized queries). This approach ensures that user input is handled safely by separating SQL logic from data, helping to prevent common injection-based attacks.
Security benefits include:
    - Protection agains SQL Injection attacks
    - Safe handling of user supplied input
    - Improved query reliability and maintainability
    - Alignment with secure coding best practices

Features  & Functionality

The system provides a fully manageable book inventory with the following capabilities:
    1.) Add New Inventory Items
        - Insert new books into the database
        - Associate existing authors or add new authors as needed
        - Specify and manage inventory quantities
    2.) View inventory
        - Display a complete list of all books currently in inventory
        - Retrieve data directly from the SQL database using secure queries
    3.) Update Inventory Records
        - Modify existing book records, including author information, quantity, and other attributes
        - Updates are performed using prepared statements to ensure data integrity
    4.) Delete Inventory Records
        - Remove books entirely from the inventory system
        - Deletions are validated and securely executed through parameterized queries
    5.) Search Inventory
        - Search for individual books using user-defined parameters (e.g., title, author)
        - Search functionality is protected agains malicious input via prepared Statements

Technical overview
    - Language: Python
    - Database: SQL (Relational Database)
    - Architecture: Menu-driven CLI application
    - Database Operations: Full CRUD
    - Security: Prepared statements for all database interactions

Learning out comes
    - Implemented secure database access patterns using prepared statements
    - Designed relational data models for inventory and author management
    - Strengthened understanding of CRUD operations and data validation
    - Applied secure coding principles in a real-world style application
