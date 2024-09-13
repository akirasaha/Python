import sqlite3

# Function to get user input for a new book with quantity error checking
def get_book_input():
    title = input("Enter the title book: ")
    author = input("Enter the author: ")

    while True: 
        try: 
            qty = int(input("Enter the quantity: "))
            break 
        except ValueError as error: 
            (print("Invalid input. Please enter an integer for the quantity!"))
    
    return title , author, qty 

# Function to display menu and get user choice
def display_menu():
    while True: 
        try: 
            user_input = int(input('''Would you like to: 
                             1 - Enter book
                             2 - Update book
                             3 - Delete book
                             4 - Search books 
                             0 - Exit 
                             Please ensure you enter a number only!
                             '''))
            
            return user_input 
        except ValueError: 
            print("Oops, please ensure you enter a number only!")


try:
    
    # Creates or opens ebookstore.db file with SQLite DB
    db = sqlite3.connect('ebookstore.db')

    # Get a cursor object
    cursor = db.cursor()

    # Creates 'book' table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS 
                   book(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, qty INTEGER)''')
    
    # Commit the change
    db.commit()

 
    # Data saved in book_details that need to be inserted into 'book' table - id , title, author, qty
    book_details = [
                    (3001,'A Tale of Two Cities','Charles Dickens',30),
                    (3002,'Harry Potter and the Philosopher\'s Stone','J.K. Rowling',40),
                    (3003,'The Lion, the Witch and the Wardrobe','C.S. Lewis',25),
                    (3004,'The Lord of the Rings','J.R.R. Tolkien',37),
                    (3005,'Alice in Wonderland','Lewis Carroll',12),
                    (3006,'Sapiens','Yuval Noah Harari',10),
                    (3007,'My Brilliant Friend','Elena Ferrante',8)
                    ]
    
    # Insert several lines of data into 'book' table
    cursor.executemany('''INSERT INTO book(id, title, author, qty)
                       VALUES(?, ?, ?, ?)''',book_details)
    
    print("Book table successfully populated with book data!")

    # Commit the change
    db.commit()

# Catch the error  
except Exception as error:
    # Rollback any change if an error occurs
    db.rollback() 

finally:
    # Close the database connection
    db.close()


print("Welcome to the ebookstore database!")


# Creates or opens ebookstore.db file with SQLite DB
db = sqlite3.connect('ebookstore.db')

# Get a cursor object
cursor = db.cursor()


try:
    while True: 
        user_input  = display_menu()

        # Get the following input from the user: title, author, qty 
        if user_input == 1: 
            # Store return values from get_book_input() function as title, author, qty
            title, author, qty  = get_book_input()

            # Insert data into the 'book' table 
            cursor.execute('''INSERT INTO book(title, author, qty) VALUES(?,?,?)'''
                           ,(title,author,qty))
        
            db.commit()

            print("Book successfully entered!")

        elif user_input == 2:

            # Get input from the user
            title = input("Enter the title of the book you would like to update: ").strip().lower()

            # Retrieve the data from 'book' table
            cursor.execute('''SELECT * FROM book''')

            # Initialize book_id
            book_id = None

            for row in cursor: 
                # If book name matches input from user
                if row[1].strip().lower() == title:
                    # Store id of book in book_id
                    book_id = row[0]
                    break 
                
            if book_id is None:
                print("Oops, book not found!") 

            else:        
                while True:
                    try:
                        # Get updated quantity value from user
                        quantity = int(input("Please enter the new quantity: "))
                        break 

                    # Ensure user enters a number
                    except ValueError as error:
                        print("Oops, please ensure you enter a number only!")
                        continue
            
                # Execute SQL query to update the qty value for the relevant row 
                cursor.execute('''UPDATE book SET qty=? WHERE id=?
                            ''',(quantity,book_id))
            
                # Commit the change
                db.commit()

                print("Quantity successfully updated!")

        
        elif user_input == 3:
            
            # Get title from user
            title = input("Enter the name of the book you would like to delete: ").strip().lower()

            # Retrieve data from 'book' table
            cursor.execute('''SELECT * FROM book''')

            # Initialize book_id
            book_id = None 

            for row in cursor: 
                # If title matches input from user 
                if row[1].lower().strip() == title:
                    # Store id of book in book_id
                    book_id = row[0]
                    break
                
            if book_id == None:
                print("Oops, book not found!")
            
            else: 
                # Execute SQL query to delete row from 'book' table 
                cursor.execute('''DELETE FROM book WHERE id=?''', (book_id,))

                # Commit the change
                db.commit()

                print(f"Book '{title}' has been deleted!")


        elif user_input == 4:

            # Get book name from user
            title = input("Enter the title of the book you're looking for: ").strip().lower() 

            # Retrieve data from 'book' table
            cursor.execute('''SELECT * FROM book''')

            # Initialize book_id
            book_id = None 

            for row in cursor: 
                # If book name matches input from the user
                if row[1].strip().lower() == title:
                    # Store id of book in book_id
                    book_id = row[0]
                    break 
            

            if book_id is None:
                print("Oops, book not found!")

            else:
                # Retrieve data from book table 
                cursor.execute('''SELECT * FROM book WHERE id=?''',(book_id,))

                # Fetch the row of data last retrieved
                row = cursor.fetchone()
    
                # check if row is not none
                if row:
                    print(f'''
                        Title: {row[1]}
                        Author: {row[2]}
                        Quantity: {row[3]}  
                          ''')
                else:
                    print("Oops, unable to retrieve data!")

        elif user_input == 0:
            print("Goodbye!")
            # Exit the program
            break 

        else:
            print("Oops, invalid input. Please enter 0, 1, 2, 3 or 4 only.")



# If a user enters invalid input print an error message 
except Exception as error:
    print("Oops, an error has occurred!")
    print(error)

finally: 
    # Close the database
    db.close()









