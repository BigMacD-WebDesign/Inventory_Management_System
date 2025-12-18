import sqlite3
from create_database_file import get_sql_cursor

# --- Create DB and get cursor ---
cursor, conn = get_sql_cursor()


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
        
        if choice == "0":
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
    
    