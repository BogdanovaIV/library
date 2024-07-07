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

    def update_row(self, row, values):
        """
        Updates a row in the worksheet.

        Args:
            row (int): The row number of the cell.
            values (list): The list of values to set in the cells.

        Returns:
            bool: True if the row was updated successfully, False otherwise.
        """
        i = 0
        while i < len(values):
            result = self.update_cell(row, i + 1, values[i])
            if not result:
                return False
            i += 1

        return True

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
    A mixin class that call input which checks the value.

    Methods:
        input_int: Input the value which is an integer.
    """

    @staticmethod
    def input_int(text_message):
        """
        Input the value which is an integer.

        Args:
            text_message (str): The message is sent to the user.
        """
        value = None
        while True:
            try:
                value = input(text_message)

                if value.lower() != "exit":
                    value = int(value)
                break

            except ValueError as e:
                print(f"Invalid data: {e}, please try again.\n")

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
        self.atrubites_name = {
            "id": "ID",
            "full_name": "FULL NAME",
            "birth_year": "BIRTH YEAR",
        }
        self.atrubites_col = {"id": 1, "full_name": 2, "birth_year": 3}
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
                record[self.atrubites_name["id"]],
                record[self.atrubites_name["full_name"]],
                record[self.atrubites_name["birth_year"]],
            )
            for record in records
        ]

    def get_all_authors_dictionary():
        """
        Retrieves all authors from the worksheet.

        Returns:
            dictionary: A dictionary of ID and full name.
        """
        records = self.get_all_records()
        return {
            record[self.atrubites_name["id"]]: record[self.atrubites_name["full_name"]]
            for record in records
        }

    def check_duplicate_data(self, full_name, birth_year):
        """
        Checks the database for duplicate data by full name and birth year.

        Returns:
            ID if it is or None if it is not.
        """
        records = self.get_all_records()
        for record in records:
            if (
                record[self.atrubites_name["full_name"]] == full_name
                and record[self.atrubites_name["birth_year"]] == birth_year
            ):
                return record[self.atrubites_name["id"]]
        return None

    def find_author(self, value):
        """
        Find the author by full name or ID.

        Returns:
            Author objects and int(row of author found) or None and None.
        """
        cells = self.find_all_cells(value)
        index = 0
        if len(cells) != 1:
            while True:
                print("Choose the author:")
                i = 0
                while i < len(cells):
                    values_row = self.get_row(cells[i].row)
                    print(
                        f'{i}. {values_row[self.atrubites_col["id"]-1]} - {values_row[self.atrubites_col["full_name"] - 1]} - {values_row[self.atrubites_col["birth_year"] - 1]}'
                    )
                    i += 1
                choice = int(input("Enter your choice: "))

                if choice >= 0 and choice < len(cells):
                    index = choice
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

        values_row = self.get_row(cells[index].row)
        return [
            Author(
                values_row[self.atrubites_col["id"] - 1],
                values_row[self.atrubites_col["full_name"] - 1],
                values_row[self.atrubites_col["birth_year"] - 1],
            ),
            cells[index].row,
        ]

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
        author_full_name (str): The author's ID.
        shelf_number (str): The number of the shelf on which the book is stored.
    """

    def __init__(self, id, title, author_id, shelf_number):
        """
        Initializes the Book class with the given details.

        Args:
            id (str): The book's ID.
            title (str): The book's title.
            author_id (str): The author's ID.
            author_full_name (str): The author's ID.
            shelf_number (str): The number of the shelf on which the book is stored.
        """
        self.id = id
        self.title = title
        self.author_id = author_id
        self.author_full_name = author_full_name
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
        self.atrubites_name = {
            "id": "ID",
            "title": "TITLE",
            "author_id": "AUTHOR (ID)",
            "shelf_number": "SHELF",
        }
        self.atrubites_col = {"id": 1, "title": 2, "author_id": 3, "shelf_number": 4}
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
                record[self.atrubites_name["id"]],
                record[self.atrubites_name["title"]],
                record[self.atrubites_name["author_id"]],
                record[self.atrubites_name["shelf_number"]],
            )
            for record in records
        ]

    def check_duplicate_data(self, title, author_id):
        """
        Checks the database for duplicate data by title and author's ID.

        Returns:
            ID if it is or None if it is not.
        """
        records = self.get_all_records()
        for record in records:
            if (
                record[self.atrubites_name["title"]] == full_name
                and record[self.atrubites_name["author_id"]] == birth_year
            ):
                return record[self.atrubites_name["id"]]
        return None

    def edit_book(self, row, book):
        """
        Updates the book in the worksheet.

        Args:
            row (int): The row number of the cells.
            author (Book object): The author contains new values.

        Returns:
            bool: True if the row was updated successfully, False otherwise.
        """
        return self.update_row(row, book.to_list())


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

            full_name = input(
                "Enter the full name or 'Exit' to back to the previous step: "
            )
            if full_name.lower() == "exit":
                break
            text_message = (
                "Enter the birth year or 'Exit' to back to the previous step: "
            )
            birth_year = self.input_int(text_message)

            if type(birth_year) == str and birth_year.lower() == "exit":
                break

            id = self.authors_manager.check_duplicate_data(full_name, birth_year)
            if id:
                print(
                    f"The database contains the author {full_name} - {birth_year}. ID is {id}"
                )
            else:
                new_author = Author(
                    self.authors_manager.generate_unique_id(), full_name, birth_year
                )
                if self.authors_manager.append_row(new_author.to_list()):
                    print(
                        f"Author {new_author.id} - {new_author.full_name} - {new_author.birth_year} added successfully."
                    )
                    break
                else:
                    print(
                        f"Failed to add author {new_author.id} - {new_author.full_name} - {new_author.birth_year}."
                    )

    def edit_author(self):
        """Edits an author."""
        while True:

            value = input(
                "Enter the full name or ID or 'Exit' to back to the previous step: "
            )
            if value.lower() == "exit":
                break

            [author, row] = self.authors_manager.find_author(value)

            text_message = f'Enter the new full name. The full name is {author.full_name} or "Exit" to back to the previous step: '
            author.full_name = self.input_int(text_message)

            if author.full_name.lower() == "exit":
                break

            text_message = (
                "Enter the birth year or 'Exit' to back to the previous step: "
            )
            birth_year = self.input_int(text_message)

            if type(birth_year) == str and birth_year.lower() == "exit":
                break

            author.birth_year = birth_year
            if self.authors_manager.edit_author(row, author):
                print(
                    f"Author {author.id} - {author.full_name} - {author.birth_year} edited successfully."
                )
                break
            else:
                print(
                    f"Failed to edit author {author.id} - {author.full_name} - {author.birth_year}."
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
                author_name = authors[books.author_id]
            except KeyError as e:
                author_name = "Invalid author's ID"
            finally:
                print(
                    f"{book.id} - {book.title} - {authors[books.author_id]} - {book.shelf}"
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

    # Create a Menu instance
    print("Welcome to Library Data Automation")
    menu = Menu(authors_manager)

    # Display the main menu
    menu.display_menu()


main()
