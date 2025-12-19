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
                cursor.execute("SELECT id FROM author WHERE id = ?", (author_id))
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
    
    