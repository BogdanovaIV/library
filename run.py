from googlesheets import GoogleSheetsClient, GoogleSheet
from authors import Author, Authors
from books import Book, Books
from mixin_classes import UniqueIDMixin, InputMixin

CREDS = GoogleSheetsClient.get_creds("creds.json")








class Menu(InputMixin):
    """
    A class representing a menu-driven interface.

    Attributes:
        authors_manager (Authors): An instance of the Authors class.
    """

    def __init__(self, authors_manager, books_manager):
        """
        Initializes the Menu class.

        Args:
            authors_manager (Authors): An instance of the Authors class.
            books_manager (Books): An instance of the Books class.
        """
        self.authors_manager = authors_manager
        self.books_manager = books_manager

    def display_menu(self):
        """Displays the main menu and handles user input."""
        while True:
            print("\nMain Menu:")
            print("1. Authors")
            print("2. Books")
            print("3. Exit")
            choice = input("Enter your choice:\n")

            if choice == "1":
                self.display_authors_menu()
            elif choice == "2":
                self.display_books_menu()
            elif choice == "3":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    # Authors menu
    def display_authors_menu(self):
        """Displays the 'authors' menu and handles user input."""
        while True:
            print("\nAuthors Menu:")
            print("1. Get all authors")
            print("2. Add a new author")
            print("3. Edit an author")
            print("4. Find books by an author")
            print("5. Back to the previous step")
            choice = input("Enter your choice:\n")

            if choice == "1":
                self.get_all_authors()
            elif choice == "2":
                self.add_new_author()
            elif choice == "3":
                self.edit_author()
            elif choice == "4":
                self.get_books_by_author()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def get_all_authors(self):
        """Displays all authors."""
        authors = self.authors_manager.get_all_authors()
        for author in authors:
            print(author.to_fstring())

    def add_new_author(self):
        """Adds a new author."""
        while True:
            # Input the full name
            full_name = self.input_str(
                "Enter the full name or 'Exit' to back to the previous step:\n"
            )
            if full_name is None:
                break
            # Input the birth year
            birth_year = self.input_int(
                "Enter the birth year or 'Exit' to back to the previous step:\n"
            )
            if birth_year is None:
                break
            # Check on duplicates
            record = self.authors_manager.check_duplicate_data(
                {
                    self.authors_manager.attributes_name["full_name"]: full_name,
                    self.authors_manager.attributes_name["birth_year"]: birth_year,
                }
            )
            if record:
                print(
                    f"The database contains the author {full_name} - {birth_year}. ID is {record[self.authors_manager.attributes_name["id"]]}"
                )
                continue
            # Add a new author to the worksheet
            new_author = Author(
                self.authors_manager.generate_unique_id(), full_name, birth_year
            )
            # Success
            if self.authors_manager.append_row(new_author.to_list()):
                print(
                    f"Author {new_author.to_fstring()} added successfully."
                )
                break
            # Failed
            print(
                f"Failed to add author {new_author.to_fstring()}."
            )

    def edit_author(self):
        """Edits an author."""
        while True:
            # Input the full name or ID
            value = self.input_str(
                "Enter the full name or ID or 'Exit' to back to the previous step:\n"
            )
            if value is None:
                break
            # Find the author by the full name or ID
            [author, row] = self.authors_manager.find_author(value)

            if author is None:
                continue
            # Input new full name
            new_full_name = self.input_str(
                "Enter the new full name or empty string not to change the full name or 'Exit' to back to the previous step:\n",
                True,
            )
            if new_full_name is None:
                break
            elif new_full_name:
                author.full_name = new_full_name
            # Input new birth year
            birth_year = self.input_int(
                "Enter the birth year or 'Exit' to back to the previous step:\n"
            )
            if birth_year is None:
                break

            author.birth_year = birth_year
            # Edit the author in the worksheet
            # Success
            if self.authors_manager.edit_author(row, author):
                print(
                    f"The author {author.to_fstring()} edited successfully."
                )
                break
            # Failed
            print(
                f"Failed to edit the author {author.to_fstring()}."
            )

    def get_books_by_author(self):
        """Gets books by an author."""
        author, row = self.get_author_and_row()
        if author is None:
            return
        
        books = self.books_manager.get_all_books_with_selection(
            {
            },
            {
                self.books_manager.attributes_name["author_id"]: author.id,
            }
        )
        if books:
            for book in books:
                print(book.to_fstring(author.full_name))
        else:
            print(f"No books found by {author.full_name}")
                


    # Books menu
    def display_books_menu(self):
        """Displays the books menu and handles user input."""
        while True:
            print("\nBooks Menu:")
            print("1. Get all books")
            print("2. Add a new book")
            print("3. Edit a book")
            print("4. Find books by part of the title")
            print("5. Back to the previous step")
            choice = input("Enter your choice:\n")

            if choice == "1":
                self.get_all_books()
            elif choice == "2":
                self.add_new_book()
            elif choice == "3":
                self.edit_book()
            elif choice == "4":
                self.get_books_by_tittle()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def print_books(self, books):
        """
        Print all books.
        
        Args:
            books (list): The lust of Book objects to print.

        """
        authors = self.authors_manager.get_all_authors_dictionary()
        for book in books:
            try:
                author_full_name = authors[book.author_id]
            except KeyError as e:
                author_full_name = "Invalid author's ID"
            finally:
                print(
                    book.to_fstring(author_full_name)
                )


    def get_all_books(self):
        """Displays all books."""
        books = self.books_manager.get_all_books()
        self.print_books(books)
              
    def get_books_by_tittle(self):
        """Gets books by a part of the title."""
        # Input the title
        title = self.input_str(
            "Enter the title:\n"
        )
        if not title:
            print("The title cannot be empty.")
        else:            
            books = self.books_manager.get_all_books_with_selection(
                {
                    self.books_manager.attributes_name["title"]: title
                },
                {
                }
            )
            if books:
                self.print_books(books)
            else:
                print("No books found.")

    def get_author_and_row(self):
        """
        Gets the author and row number based on user input.

        Returns:
            tuple: (Author, int) if author is found, where Author is the Author object
                and integer is the row number in the worksheet.
            None, None if the user exits or the author is not found.
        """
        while True:
            value = self.input_str(
                "Enter the full name or ID of the author or 'Exit' to go back: "
            )
            if value is None:
                return None, None

            author, row_author = self.authors_manager.find_author(value)
            if author:
                return author, row_author
            else:
                print(f"Author '{value}' not found.")

    def add_new_book(self):
        """Adds a new book."""
        while True:
            # Find the author
            author, row = self.get_author_and_row()
            if author is None:
                return

            # Input the title
            title = self.input_str(
                "Enter the title or 'Exit' to back to the previous step:\n"
            )
            if title == "exit":
                break
            # Check on duplicates
            record = self.books_manager.check_duplicate_data(
                {
                    self.books_manager.attributes_name["title"]: title,
                    self.books_manager.attributes_name["author_id"]: author.id,
                }
            )
            if record:
                print(
                    f"The database contains the book {title} - {author.full_name}. ID is {record[self.books_manager.attributes_name["id"]]}"
                )

                continue
            # Input the number of the shelf
            shelf_number = self.input_int(
                "Enter the number of the shelf on which the book is stored or 'Exit' to back to the previous step:\n"
            )

            if shelf_number is None:
                break
            # Add a new book to the worksheet
            new_book = Book(
                self.books_manager.generate_unique_id(), title, author.id, shelf_number
            )
            # Success
            if self.books_manager.append_row(new_book.to_list()):
                print(
                    f"The book {new_book.to_fstring(author.full_name)} added successfully."
                )
                break
            else:
                # Failed
                print(
                    f"Failed to add the book {new_book.to_fstring(author.full_name)}."
                )

    def find_book(self, author):
        """
        Finds the book and its row number based on user input.

        Args:
            author (Author): The Author object for whom to find the book.

        Returns:
            tuple: (Book, int) if book is found, where Book is the Book object
                and integer is the row number in the worksheet.
            None, None if the user exits or the book is not found.
        """

        while True:
            value = self.input_str(
                "Enter the title or ID of the book or 'Exit' to go back: "
            )
            if value is None:
                return None, None

            book, row = self.books_manager.find_book(value, author.id, author.full_name)
            if book:
                return book, row
            else:
                print(f"The book {value} - {author.full_name} is not found")

    def edit_book(self):
        """Edits a book."""
        # Find the author
        author, row_author = self.get_author_and_row()
        if author is None:
            return
        # Find the book
        book, row = self.find_book(author)
        if book is None:
            return

        while True:
            # Input the new title
            new_title = self.input_str(
                "Enter the new title or leave empty to keep the existing title:\n", True
            )
            if new_title is None:
                break

            if new_title:
                book.title = new_title
            # Input the new shelf number
            shelf_number = self.input_int(
                "Enter the shelf number or 'Exit' to go back:\n"
            )
            if shelf_number is None:
                break

            book.shelf_number = shelf_number
            # Update the book
            # Success
            if self.books_manager.update_row(row, book.to_list()):
                print(
                    f"The book {book.to_fstring(author.full_name)} edited successfully."
                )
                break
            # Failed
            else:
                print(
                    f"Failed to edit the book {book.to_fstring(author.full_name)}."
                )


def main():
    """
    Run all program functions
    """
    sheet_name = "library"

    # Initialize the client and open the worksheet
    client = GoogleSheetsClient(CREDS)

    # Initialize the Authors manager
    authors_manager = Authors(client.open_worksheet(sheet_name, "authors"))

    # Initialize the Books manager
    books_manager = Books(client.open_worksheet(sheet_name, "books"))

    # Create a Menu instance
    print("Welcome to Library Data Automation")
    menu = Menu(authors_manager, books_manager)

    # Display the main menu
    menu.display_menu()


main()
