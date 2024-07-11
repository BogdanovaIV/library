import gspread
from google.oauth2.service_account import Credentials
import uuid


class GoogleSheetsClient:
    """
    A client class to handle authentication and connection to Google Sheets.

    Attributes:
        creds_file (str): Path to the credentials JSON file.
        client (gspread.Client): An authenticated gspread client.
    """

    def __init__(self, creds):
        """
        Initializes the GoogleSheetsClient with the given credentials.

        Args:
            creds (google.oauth2.service_account.Credentials): The credentials for authentication.
        """
        self.client = self.authenticate(creds)

    def get_creds(creds_file):
        """
        Generates credentials from the service account file.

        Args:
            creds_file (str): Path to the credentials JSON file.

        Returns:
            google.oauth2.service_account.Credentials: The generated credentials.
        """
        return Credentials.from_service_account_file(
            creds_file,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive",
            ],
        )

    def authenticate(self, creds):
        """
        Authenticates the client using the provided credentials.

        Args:
            creds (google.oauth2.service_account.Credentials): The credentials for authentication.

        Returns:
            gspread.Client: An authenticated gspread client.
        """
        return gspread.authorize(creds)

    def open_worksheet(self, sheet_name, worksheet):
        """
        Opens a specific worksheet from a Google Sheet.

        Args:
            sheet_name (str): The name of the Google Sheet.
            worksheet (str): The name of the worksheet within the Google Sheet.

        Returns:
            gspread.models.Worksheet: The worksheet object.
        """
        return self.client.open(sheet_name).worksheet(worksheet)


CREDS = GoogleSheetsClient.get_creds("creds.json")


class GoogleSheet:
    """
    A class to handle operations on a specific Google Sheet worksheet.

    Attributes:
        sheet (gspread.models.Worksheet): The worksheet object.
    """

    def __init__(self, sheet):
        """
        Initializes the GoogleSheet class with a worksheet object.

        Args:
            sheet (gspread.models.Worksheet): The worksheet object.
        """
        self.sheet = sheet

    def get_all_records(self):
        """
        Retrieves all records from the worksheet.

        Returns:
            list: A list of dictionaries containing all records.
        """
        return self.sheet.get_all_records()

    def get_row(self, index):
        """
        Retrieves a specific row from the worksheet.

        Args:
            index (int): The index of the row to retrieve.

        Returns:
            list: A list containing the values in the row.
        """
        return self.sheet.row_values(index)

    def update_cell(self, row, col, value):
        """
        Updates a specific cell in the worksheet.

        Args:
            row (int): The row number of the cell.
            col (int): The column number of the cell.
            value (str): The value to set in the cell.

        Returns:
            bool: True if the cell was updated successfully, False otherwise.
        """
        try:
            self.sheet.update_cell(row, col, value)
            print("Cell updated successfully.")
            return True
        except gspread.exceptions.APIError as e:
            print(f"Failed to update cell: {e}")
            return False

    def update_row(self, row, values_list):
        """
        Updates a row in the worksheet.

        Args:
            row (int): The row number of the cell.
            values_list (list): The list of values to set in the cells.

        Returns:
            bool: True if the row was updated successfully, False otherwise.
        """
        try:
            self.sheet.update(range_name=f"A{row}:Z{row}", values=[values_list])
            print("Row updated successfully.")
            return True
        except Exception as e:
            print(f"Failed to update row: {e}")
            return False

    def append_row(self, values):
        """
        Appends a new row to the worksheet.

        Args:
            values (list): A list of values to append as a new row.

        Returns:
            bool: True if the row was appended successfully, False otherwise.
        """
        try:
            self.sheet.append_row(values)
            print("Row appended successfully.")
            return True
        except gspread.exceptions.APIError as e:
            print(f"Failed to append row: {e}")
            return False

    def find_in_column(self, col, value):
        """
        Finds a value in a specific column of the worksheet.

        Args:
            col (int): The column number to search in.
            value (str): The value to search for.

        Returns:
            gspread.models.Cell or None: The cell containing the value, or None if not found.
        """
        cell = self.sheet.find(value, in_column=col)
        return cell

    def find_all_cells(self, value):
        """
        Finds all cells that match a specific value in the worksheet.

        Args:
            value (str): The value to search for.

        Returns:
            list: A list of gspread.models.Cell objects that match the value.
        """
        return self.sheet.findall(value)

    def find_cells_contain_value(self, attributes):
        """
        Finds all cells that match a specific value in the worksheet.

        Args:
            attributes (dict): A dictionary where the key is an attribute and the value is the value being tested.


        Returns:
            list: A list of gspread.models.Cell objects that match the value.
        """
        records = self.sheet.get_all_records()
        matching_records = []
        for row, record in enumerate(records, start=2):
            if any(
                value.lower() in record.get(attr).lower()
                for attr, value in attributes.items()
            ):
                matching_records.append([row, record])
        return matching_records

    def check_duplicate_data(self, attributes):
        """
        Checks the database for duplicate data by specified attributes.

        Args:
            attributes (dict): A dictionary where the key is an attribute and the value is the value being tested.

        Returns:
            dict: The record if a duplicate is found, otherwise None.
        """
        records = self.get_all_records()
        for record in records:
            if all(record.get(attr) == value for attr, value in attributes.items()):
                return record
        return None


class UniqueIDMixin:
    """
    A mixin class that generates unique IDs.

    Methods:
        generate_unique_id: Generates a new unique ID.
    """

    @staticmethod
    def generate_unique_id():
        """
        Generates a new unique ID.

        Returns:
            str: A unique ID string.
        """
        return str(uuid.uuid4())


class InputMixin:
    """
    A mixin class that calls input which checks the value.

    Methods:
        input_int: Input the value which is an integer.
    """

    @staticmethod
    def input_int(text_message):
        """
        Input the value which is an integer.

        Args:
            text_message (str): The message is sent to the user.

        Returns:
            integer or None: The value inputted by the user.
        """
        value = None
        while True:
            try:
                value = input(text_message)

                if value.lower() == "exit":
                    value = None
                else:
                    value = int(value)

            except ValueError as e:
                print(f"Invalid data: {e}, please try again.\n")
            else:
                break

        return value

    @staticmethod
    def input_str(text_message, empty_str_avaliable=False):
        """
        Input the value which is a string.

        Args:
            text_message (str): The message is sent to the user.

        Returns:
            string or None: The value inputted by the user.
        """
        value = None
        while True:
            try:
                value = input(text_message)

                if not empty_str_avaliable and not value:
                    raise ValueError("Value cannot be empty")
                elif value.lower() == "exit":
                    value = None

            except ValueError as e:
                print(f"Invalid data: {e}, please try again.\n")
            else:
                break

        return value


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
        # Use the dictionary to have the feature to quickly change column's position
        self.attributes_name = {
            "id": "ID",
            "full_name": "FULL NAME",
            "birth_year": "BIRTH YEAR",
        }
        self.attributes_col = {"id": 1, "full_name": 2, "birth_year": 3}
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
        cells = self.find_cells_contain_value(
            {
                self.attributes_name["id"]: value,
                self.attributes_name["full_name"]: value,
            },
        )

        if not cells:
            print(f"The author with {value} is not found.\n")
            return None, -1

        if len(cells) == 1:
            index = 0
        else:
            index = self.choose_author(cells)

        values_row = cells[index][1]
        return (
            Author(
                values_row[self.attributes_name["id"]],
                values_row[self.attributes_name["full_name"]],
                values_row[self.attributes_name["birth_year"]],
            ),
            cells[index][0],
        )

    def choose_author(self, cells):
        """
        Prompts the user to choose an author from multiple matches.

        Args:
            cells (list): List of matched cells.

        Returns:
            int: The index of the chosen author.
        """
        while True:
            print("Choose the author:")
            for i, cell in enumerate(cells, start=1):
                values_row = cell[1]
                print(
                    f'{i}. {values_row[self.attributes_name["id"]]} - {values_row[self.attributes_name["full_name"]]} - {values_row[self.attributes_name["birth_year"]]}'
                )
            try:
                choice = int(input("Enter your choice: "))
                if 0 < choice <= len(cells):
                    return choice - 1

                raise ValueError("Please enter a valid option.")
            except ValueError as e:
                print(f"Invalid data: {e}, please try again.\n")

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
        # Use the dictionary to have the feature to quickly change column's position
        self.attributes_name = {
            "id": "ID",
            "title": "TITLE",
            "author_id": "AUTHOR (ID)",
            "shelf_number": "SHELF",
        }
        self.attributes_col = {"id": 1, "title": 2, "author_id": 3, "shelf_number": 4}
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

    def find_book(self, value, author_id):
        """
        Checks the database for a book by title or ID and author's ID.

        Args:
            value (str): The book's title or ID.
            author_id (str): The author's ID.

        Returns:
            Book: The found Book object.
            int: The row number where the book was found.
            or
            None: If no book was found.
            int: -1 if no book was found.
        """
        records = self.get_all_records()
        for row, record in enumerate(
            records, start=2
        ):  # start=2 to account for the header row
            if (record.get(self.attributes_col["author_id"]) == author_id) and (
                record.get(self.attributes_col["id"]) == value
                or record.get(self.attributes_col["title"]) == value
            ):
                return (
                    Book(
                        record.get(self.attributes_col["id"]),
                        record.get(self.attributes_col["title"]),
                        record.get(self.attributes_col["author_id"]),
                        record.get(self.attributes_col["shelf_number"]),
                    ),
                    row,
                )

        return None, -1


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
            choice = input("Enter your choice: ")

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
            choice = input("Enter your choice: ")

            if choice == "1":
                self.get_all_authors()
            elif choice == "2":
                self.add_new_author()
            elif choice == "3":
                self.edit_author()
            elif choice == "4":
                self.find_books_by_author()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def get_all_authors(self):
        """Displays all authors."""
        authors = self.authors_manager.get_all_authors()
        for author in authors:
            print(f"{author.id} - {author.full_name} - {author.birth_year}")

    def add_new_author(self):
        """Adds a new author."""
        while True:
            # Input the full name
            full_name = self.input_str(
                "Enter the full name or 'Exit' to back to the previous step: "
            )
            if full_name == None:
                break
            # Input the birth year
            birth_year = self.input_int(
                "Enter the birth year or 'Exit' to back to the previous step: "
            )
            if birth_year == None:
                break
            # check on duplicates
            record = self.authors_manager.check_duplicate_data(
                {
                    self.authors_manager.attributes_name["full_name"]: full_name,
                    self.authors_manager.attributes_name["birth_year"]: birth_year,
                }
            )
            if record:
                print(
                    f"The database contains the author {full_name} - {birth_year}. ID is {record['id']}"
                )
                continue
            # Add a new author in the worksheet
            new_author = Author(
                self.authors_manager.generate_unique_id(), full_name, birth_year
            )
            # Success
            if self.authors_manager.append_row(new_author.to_list()):
                print(
                    f"Author {new_author.id} - {new_author.full_name} - {new_author.birth_year} added successfully."
                )
                break
            # Failed
            print(
                f"Failed to add author {new_author.id} - {new_author.full_name} - {new_author.birth_year}."
            )

    def edit_author(self):
        """Edits an author."""
        while True:
            # Input the full name or ID
            value = self.input_str(
                "Enter the full name or ID or 'Exit' to back to the previous step: "
            )
            if value == None:
                break
            # Find the author by the full name or ID
            [author, row] = self.authors_manager.find_author(value)

            if author == None:
                continue
            # Input new full name
            new_full_name = self.input_str(
                "Enter the new full name or empty string not to change the full name or 'Exit' to back to the previous step: ",
                True,
            )
            if new_full_name == None:
                break
            elif new_full_name:
                author.full_name = new_full_name
            # Input new birth year
            birth_year = self.input_int(
                "Enter the birth year or 'Exit' to back to the previous step: "
            )
            if birth_year == None:
                break

            author.birth_year = birth_year
            # Edit the author in the worksheet
            # Success
            if self.authors_manager.edit_author(row, author):
                print(
                    f"The author {author.id} - {author.full_name} - {author.birth_year} edited successfully."
                )
                break
            # Failed
            print(
                f"Failed to edit the author {author.id} - {author.full_name} - {author.birth_year}."
            )

    def find_books_by_author(self):
        """Finds books by an author."""

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
            choice = input("Enter your choice: ")

            if choice == "1":
                self.get_all_books()
            elif choice == "2":
                self.add_new_book()
            elif choice == "3":
                self.edit_book()
            elif choice == "4":
                self.find_books_by_title()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def get_all_books(self):
        """Displays all books."""
        books = self.books_manager.get_all_books()
        authors = self.authors_manager.get_all_authors_dictionary()
        for book in books:
            try:
                author_name = authors[book.author_id]
            except KeyError as e:
                author_name = "Invalid author's ID"
            finally:
                print(
                    f"{book.id} - {book.title} - {author_name} - shelf ({book.shelf_number})"
                )

    def add_new_book(self):
        """Adds a new book."""
        while True:
            # Input the full name or ID of the author
            value = self.input_str(
                "Enter the full name or ID of the author or 'Exit' to back to the previous step: "
            )
            if value == None:
                break
            # Find the author
            [author, row] = self.authors_manager.find_author(value)

            if author == None:
                continue
            # Input the title
            title = self.input_str(
                "Enter the title or 'Exit' to back to the previous step: "
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
                "Enter the number of the shelf on which the book is stored or 'Exit' to back to the previous step: "
            )

            if shelf_number == None:
                break
            # Add a new book to the worksheet
            new_book = Book(
                self.books_manager.generate_unique_id(), title, author.id, shelf_number
            )
            # Success
            if self.books_manager.append_row(new_book.to_list()):
                print(
                    f"The book {new_book.id} - {new_book.title} - {author.full_name} - shelf ({new_book.shelf_number}) added successfully."
                )
                break
            # Failed
            print(
                f"Failed to add the book {new_book.id} - {new_book.title} - {author.full_name} - shelf ({new_book.shelf_number})."
            )

    def edit_book(self):
        """Edits a book."""
        while True:
            # Input the full name and ID of the author
            value = input(
                "Enter the full name or ID of the author or 'Exit' to back to the previous step: "
            )
            if value.lower() == "exit":
                break
            # Find the author
            [author, row_author] = self.authors_manager.find_author(value)

            if type(author) == str and author.lower() == "continue":
                continue

            book = None
            row = None
            while True:
                value = input(
                    "Enter the title or ID or 'Exit' to back to the previous step: "
                )
                if value.lower() == "exit":
                    book = "exit"
                    break

                [book, row] = self.books_manager.find_book(value, author.id)

                if book:
                    break
                print(f"The book {value} - {author.full_name} is not found")

            if type(book) == str and book.lower() == "exit":
                break

            new_title = input(
                "Enter the new title or empty string not to change the title or 'Exit' to back to the previous step: "
            )
            if new_title.lower() == "exit":
                break

            if new_title:
                book.title = new_title

            text_message = "Enter the number of the shelf on which the book is stored or 'Exit' to back to the previous step: "
            shelf_number = self.input_int(text_message)

            if type(shelf_number) == str and shelf_number.lower() == "exit":
                break

            book.shelf_number = shelf_number
            if self.books_manager.update_row(row, book.to_list()):
                print(
                    f"The book {book.id} - {book.title} - {author.full_name} - shelf ({book.shelf_number}) edited successfully."
                )
                break
            else:
                print(
                    f"Failed to edit the book {book.id} - {book.title} - {author.full_name} - shelf ({book.shelf_number})."
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
