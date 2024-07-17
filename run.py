from googlesheets import GoogleSheetsClient, GoogleSheet
from mixin_classes import UniqueIDMixin, InputMixin

CREDS = GoogleSheetsClient.get_creds("creds.json")




class Author:
    """
    Represents an individual author.

    Attributes:
        id (str): The author's ID.
        full_name (str): The author's full name.
        birth_year (int): The author's birth year.
    """

    def __init__(self, id, full_name, birth_year):
        """
        Initializes the Author class with the given details.

        Args:
            id (str): The author's ID.
            full_name (str): The author's full name.
            birth_year (int): The author's birth year.
        """
        self.id = id
        self.full_name = full_name
        self.birth_year = birth_year

    def to_list(self):
        """
        Converts the author's details to a list.

        Returns:
            list: A list containing the author's details.
        """
        return [self.id, self.full_name, self.birth_year]

    def to_fstring(self):
        """
        Converts the author's details to a f-string.

        Returns:
            f-string: A f-string containing the author's details.
        """
        return f"{self.id} - {self.full_name} - {self.birth_year}"


class Authors(UniqueIDMixin, GoogleSheet):
    """
    Manages a collection of authors in a Google Sheets document.

    Inherits from GoogleSheet.
    """

    def __init__(self, sheet):
        """
        Initializes the Authors class.

        Args:
            sheet (gspread.models.Worksheet): The worksheet object.
        """
        # Use the dictionary to have the feature to quickly change a column's position
        self.attributes_name = {
            "id": "ID",
            "full_name": "FULL NAME",
            "birth_year": "BIRTH YEAR",
        }
 
        super().__init__(sheet)

    def get_all_authors(self):
        """
        Retrieves all authors from the worksheet.

        Returns:
            list: A list of Author objects.
        """
        records = self.get_all_records()
        return [
            Author(
                record[self.attributes_name["id"]],
                record[self.attributes_name["full_name"]],
                record[self.attributes_name["birth_year"]],
            )
            for record in records
        ]

    def get_all_authors_dictionary(self):
        """
        Retrieves all authors from the worksheet.

        Returns:
            dictionary: A dictionary of ID and full name.
        """
        records = self.get_all_records()
        return {
            record.get(self.attributes_name["id"]): record.get(
                self.attributes_name["full_name"]
            )
            for record in records
        }

    def find_author(self, value):
        """
        Find the author by full name or ID.

        Args:
            value (str or int): The full name or ID of the author to find.

        Returns:
            Author: The found Author object.
            int: The row number where the author was found.
            or
            None if no author was found.
            int: -1 if no author was found.
        """
        print_lambda = (
            lambda i, values_row: f'{i}. {values_row[self.attributes_name["id"]]} - {values_row[self.attributes_name["full_name"]]} - {values_row[self.attributes_name["birth_year"]]}'
        )
        values_row, index = self.find_item(
            {
                self.attributes_name["id"]: value,
                self.attributes_name["full_name"]: value,
            },
            {},
            "author",
            print_lambda,
        )
        if values_row is None:
            author = values_row
        else:
            author = Author(
                values_row[self.attributes_name["id"]],
                values_row[self.attributes_name["full_name"]],
                values_row[self.attributes_name["birth_year"]],
            )
            
        if author:
            print(f"The author is {author.to_fstring()}")
            
        return (
            author,
            index,
        )

    def edit_author(self, row, author):
        """
        Updates the author in the worksheet.

        Args:
            row (int): The row number of the cells.
            author (Author object): The author contains new values.

        Returns:
            bool: True if the row was updated successfully, False otherwise.
        """
        return self.update_row(row, author.to_list())


class Book:
    """
    Represents a book.

    Attributes:
        id (str): The book's ID.
        title (str): The book's title.
        author_id (str): The author's ID.
        shelf_number (str): The number of the shelf on which the book is stored.
    """

    def __init__(self, id, title, author_id, shelf_number):
        """
        Initializes the Book class with the given details.

        Args:
            id (str): The book's ID.
            title (str): The book's title.
            author_id (str): The author's ID.
            shelf_number (str): The number of the shelf on which the book is stored.
        """
        self.id = id
        self.title = title
        self.author_id = author_id
        self.shelf_number = shelf_number

    def to_list(self):
        """
        Converts the book's details to a list.

        Returns:
            list: A list containing the book's details.
        """
        return [self.id, self.title, self.author_id, self.shelf_number]

    def to_fstring(self, author_full_name):
        """
        Converts the book's details to a f-string.

        Args:
            author_full_name (str): The author's full name.

        Returns:
            f-string: A f-string containing the book's details.
        """
        return f"{self.id} - {self.title} - {author_full_name} - shelf ({self.shelf_number})"


class Books(UniqueIDMixin, GoogleSheet):
    """
    Manages a collection of books in a Google Sheets document.

    Inherits from GoogleSheet.
    """

    def __init__(self, sheet):
        """
        Initializes the Books class.

        Args:
            sheet (gspread.models.Worksheet): The worksheet object.
        """
        # Use the dictionary to have the feature to quickly change a column's position
        self.attributes_name = {
            "id": "ID",
            "title": "TITLE",
            "author_id": "AUTHOR (ID)",
            "shelf_number": "SHELF",
        }
 
        super().__init__(sheet)

    def get_all_books(self):
        """
        Retrieves all books from the worksheet.

        Returns:
            list: A list of Book objects.
        """
        records = self.get_all_records()
        return [
            Book(
                record[self.attributes_name["id"]],
                record[self.attributes_name["title"]],
                record[self.attributes_name["author_id"]],
                record[self.attributes_name["shelf_number"]],
            )
            for record in records
        ]

    def get_all_books_with_selection(self, attributes_any, attributes_all):
        """
        Get all books with section.

        Args:
            attributes_any (dict): A dictionary where the key is an attribute and the value is the value being tested. To match though one of them has to be equal.
            attributes_all (dict): A dictionary where the key is an attribute and the value is the value being tested. To match all of them have to be equal.

        Returns:
            List of Book objects: The list of Book objects.
        """
        cells = self.find_cells_contain_value(attributes_any, attributes_all)
        books = []
        for cell in cells:
            books.append(
                Book(
                    cell[1][self.attributes_name["id"]],
                    cell[1][self.attributes_name["title"]],
                    cell[1][self.attributes_name["author_id"]],
                    cell[1][self.attributes_name["shelf_number"]],
                )
            )
        return books

    def edit_book(self, row, book):
        """
        Updates the book in the worksheet.

        Args:
            row (int): The row number of the cells.
            book (Book object): The book contains new values.

        Returns:
            bool: True if the row was updated successfully, False otherwise.
        """
        return self.update_row(row, book.to_list())

    def find_book(self, value, author_id, author_full_name):
        """
        Checks the database for a book by title or ID and author's ID.

        Args:
            value (str): The book's title or ID.
            author_id (str): The author's ID.
            author_full_name (str): The author's full name.

        Returns:
            Book: The found Book object.
            int: The row number where the book was found.
            or
            None: If no book was found.
            int: -1 if no book was found.
        """
        print_lambda = (
            lambda i, values_row: f'{i}. {values_row[self.attributes_name["id"]]} - {values_row[self.attributes_name["title"]]}'
        )
        values_row, index = self.find_item(
            {
                self.attributes_name["id"]: value,
                self.attributes_name["title"]: value,
            },
            {
                self.attributes_name["author_id"]: author_id,
            },
            "book",
            print_lambda,
        )
        if values_row is None:
            book = values_row
        else:
            book = Book(
                values_row.get(self.attributes_name["id"]),
                values_row.get(self.attributes_name["title"]),
                values_row.get(self.attributes_name["author_id"]),
                values_row.get(self.attributes_name["shelf_number"]),
            )
        
        if book:
            print(f"The book is {book.to_fstring(author_full_name)}")
        return (
            book,
            index,
        )


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
