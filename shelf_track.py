import sqlite3
from create_database_file import get_sql_cursor

# --- Create DB and get cursor ---
cursor, conn = get_sql_cursor()


def enter_book():
    """Adding new book to DB inventory."""
    print("\n--- Add New Book ---")
    try:
        book_id = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        
        # Show existing authors
        cursor.execute("SELECT id, name, country FROM author")
        authors = cursor.fetchall()
        
        if authors:
            print("\nCurrent authors in database: ")
            for a in authors:
                print(f"{a[0]} - {a[1]} ({a[2]})")
            else:
                print("\nNo authors found yet.")
                
            print("\nOptions:")
            print("1. Choose existing author")
            print("2. Add a new author")
            
            author_choice = input("Select option (1 or 2): ")
            
            # Choose from existing authors
            if author_choice == "1":
                author_id = int(input("Enter the Author ID from the list above: "))
                # Validating ID exists:
                cursor.execute("SELECT id FROM author WHERE id = ?", (author_id,))
                if not cursor.fetchone():
                    print("Author ID not found.")
                    return
            
            # Add new author if needed
            elif author_choice == "2":
                author_id = int(input("Enter new Author, 4-digit ID: "))
                name = input("Enter Author's name: ")
                country = input("Enter Author's country: ")
                cursor.execute("INSERT INTO author (id, name, country) VALUES (?, ?, ?)", 
                               (author_id, name, country,))
                conn.commit()
                print(f"Author '{name}' added successfully!")
            else:
                print("Invalid choice.")
                return
            
            # Adding the book linked to that author
            quantity = int(input("Enter quantity: "))
            cursor.execute(
                "INSERT INTO book VALUES (?, ?, ?, ?)",
                (book_id, title, author_id, quantity)
            )
            conn.commit()
            print(f"Book '{title}' added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Book ID already exists.")
    except ValueError:
        print("Error: Invalid input. ID, author ID and qty must be numbers.") 


def view_all_books():
    """View all books in inventory"""
    print("="*50)
    print("\n--- ALL BOOKS --- \n")
    print("="*50 + "\n")
    cursor.execute("""
        SELECT book.id, book.title, author.name, book.qty
        FROM book
        INNER JOIN author
        ON book.author_id = author.id
    """)
    
    books = cursor.fetchall()
    
    if not books:
        print("No books in inventory.")
        return
    else:
        print(f"{'ID':<10}{'Title':<50}{'AuthorID':<25}{'Qty':<10}")
        print("="*100 + "\n")
        for book_id, title, author_name, qty in books:
            print(f"{book_id:<10}{title:<50}{author_name:<25}{qty:<25}")
            print("\n")


def update_book():
    """Update book info based on title"""
    print("\n--- Update Book ---")
    try:
        book_id = input("Enter book ID to update: ")
        
        # Check if book exists
        cursor.execute("SELECT * FROM book WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        
        if not book:
            print("Book not found.")
            return
        
        print(f"\nCurrent info: ID: {book[0]}, Title='{book[1]}', Author={book[2]}, Qty={book[3]}")
        print("\nWhat would you like to update?")
        print("1. Title")
        print("2. Author")
        print("3. Quantity")
        print("0. Cancel and return to main menu")
        choice = input("Enter choice (default is 0 to cancel): ") or "0"
        
        if choice == "1":
            new_title = input("Enter new title: ")
            cursor.execute("UPDATE book SET title = ? WHERE id = ?", (new_title, book_id))
            print("Title updated successfully!")
        elif choice == "2":
            cursor.execute("""
                SELECT author.id, author.name, author.country
                FROM author
                JOIN book ON book.author_id = author.id
                WHERE book.id = ?               
            """, (book_id,))
            author = cursor.fetchone()
            
            if not author:
                print("Author not found for this book.")
                return
            print(f"\nCurrent Author Info: ")
            print(f"ID: {author[0]}, Name: {author[1]}, Country: {author[2]}")
            
            # Prompt for new details (Blank = keep old)
            new_name = input("Enter new author name (Leave blank to keep current):") or author[1]
            new_country = input("Enter new author country (Leave blank to keep current):") or author[2]
            
            cursor.execute("UPDATE author SET name = ?, country = ? WHERE id = ?",
                           (new_name, new_country, author[0]))
            print("Author updated successfully")
        elif choice == "3":
            new_quantity = int(input("Enter the updated quantity: "))
            cursor.execute("UPDATE book SET qty = ? WHERE id = ?", (new_quantity, book_id))
            print("Quantity updated")
        elif choice == "0":
            print("Returning to main menu...")
            return
        else:
            print("Invalid Choice.")
            return
        
        conn.commit()
    except ValueError:
        print("Invalid input. Please enter valid numbers")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


def delete_book():
    """Deletes book from the db"""
    print("\n--- DELETE BOOK ---")
    
    title = input("Enter title to delete: ")
    
    # Check if book exists
    cursor.execute("SELECT * FROM book WHERE title LIKE ?", (f"%{title}%",))
    results = cursor.fetchall()
    
    if not results:
        print("Book not found")
        return
    
    if len(results) == 1:
        # Only one match found
        book = results[0]
        print(f"\nFound: ID={book[0]}, Title='{book[1]}', Author={book[2]}, Qty={book[3]}")
        confirm = input("Delete this book? (Yes/No): ").lower()
        
        if confirm == "yes":
            cursor.execute("DELETE FROM book WHERE id = ?", (book[0],))
            conn.commit()
            print("Book deleted successfully!")
        else:
            print("Deletion cancelled.")
    else:
        # Multiple matches - let user choose
        print(f"\n Found {len(results)} books:")
        for i, book in enumerate(results, 1):
            print(f"{i}. [{book[0]}] '{book[1]}' - Author: {book[2]}, Qty: {book[3]}")
        
        try:
            choice = int(input("\nWhich book to delete? (0 to cancel): "))
            if choice == 0:
                print("Deletion cancelled!")
                return
            if 1 <= choice <= len(results):
                book = results[choice - 1]
                confirm = input(f"Delete '{book[1]}'? (Yes/No): ").lower()
                if confirm == 'yes':
                    cursor.execute("DELETE FROM book WHERE id = ?", (book[0],))
                    conn.commit()
                    print("Book deleted successfully!")
                else:
                    print("Deletion Cancelled.")
            else:
                print("Invalid input.")
        except ValueError:
            print("Invalid input.")


def search_books():
    """Search book by titles."""
    print("\n--- Search by Title ---")
    title = input("Enter the title you want to search: ")
    
    cursor.execute("SELECT * FROM book WHERE title LIKE ?", (f"%{title}%",))
    books = cursor.fetchall()
    
    if not books:
        print("Book not found.")
    else:
        for book in books:
            print(f"\nFound: ID:{book[0]}, Title:'{book[1]}', Author:{book[2]}, QTY:{book[3]}\n")


# --- Menu ---
def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("BOOKSTORE INVENTORY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add new book")
    print("2. View all books")
    print("3. Update book")
    print("4. Delete book")
    print("5. Search book")
    print("0. Exit")
    print("="*50 + "\n")
    

def main():
    """Main Program loop"""
    
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        print("\n")
        
        if choice == "1":
            enter_book()
        elif choice == "2":
            view_all_books()
        elif choice == "3":
            update_book()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            search_books()
        elif choice == "0":
            print("You have chosen Option 0")
            print("Goodbye")
            try:
                conn.close()
                print("Database connection closed.")
            except sqlite3.Error as e:
                print(f"Warning: Database connection may not have closed properly. ({e})")
            break
        else:
            print("Invalid choice. Please select from menu options.")
            

if __name__ == "__main__":
    main()
    choice = input("Enter your choice: ")
    
    