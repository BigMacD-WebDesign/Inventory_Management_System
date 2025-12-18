""""This module provides a function to connect to a SQLite database,"""
import sqlite3


def get_sql_cursor():
    """
    Establishes a connection to "StudentDatabase.db", sets up the database
    schema by dropping any existing "Student" table, creating a new one,
    and inserting initial data. Returns a cursor for further database
    operations.

    Returns:
        sqlite3.Cursor: Cursor for database interaction.
    """
    conn = sqlite3.connect("ebookstore.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    with open("SQLFiles/create_book_table.sql",
              encoding='utf-8') as create_book_file:
        sql_script = create_book_file.read()
        
        for stmt in sql_script.split(";"):
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt + ";")
                
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM author")
    count = cursor.fetchone()[0]
    
    if count == 0:
        with open("SQLFiles/insert_book_data.sql",
                encoding='utf-8') as insert_book_file:
            insert_script = insert_book_file.read()
        
            for statement in insert_script.split(";"):
                stmt = statement.strip()
                if stmt:
                    try:
                        cursor.execute(stmt + ";")
                    except sqlite3.IntegrityError as e:
                        print(f"Warning: {e}")
                    except sqlite3.OperationalError as e:
                        print(f"SQL error: {e}")
            
        conn.commit()
        
    return cursor, conn

