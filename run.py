import gspread
from google.oauth2.service_account import Credentials


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
        """
        self.sheet.update_cell(row, col, value)

    def append_row(self, values):
        """
        Appends a new row to the worksheet.

        Args:
            values (list): A list of values to append as a new row.
        """
        self.sheet.append_row(values)

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


class Author:
    """
    Represents an individual author.

    Attributes:
        id (int): The author's ID.
        full_name (str): The author's full name.
        birth_year (int): The author's birth year.
    """

    def __init__(self, id, full_name, birth_year):
        """
        Initializes the Author class with the given details.

        Args:
            id (int): The author's ID.
            full_name (str): The author's full name.
            birth_year (int): The author's birth year.
        """
        self.id = id
        self.full_name = full_name
        self.birth_year = birth_year

    def to_list(self):
        """
        Converts the author details to a list.

        Returns:
            list: A list containing the author's details.
        """
        return [self.id, self.full_name, self.birth_year]


class Authors(GoogleSheet):
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
                record[atrubites_col["id"]],
                record[atrubites_col["full_name"]],
                record[atrubites_col["birth_year"]],
            )
            for record in records
        ]


class Menu:
    """
    A class representing a menu-driven interface.

    Attributes:
        authors_manager (Authors): An instance of the Authors class.
    """

    def __init__(self, authors_manager):
        """
        Initializes the Menu class.

        Args:
            authors_manager (Authors): An instance of the Authors class.
        """
        self.authors_manager = authors_manager

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
                print("Block under development!")
                pass
            elif choice == "3":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def display_authors_menu(self):
        """Displays the authors menu and handles user input."""
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

    def add_new_author(self):
        """Adds a new author."""

    def edit_author(self):
        """Edits an author."""

    def find_books_by_author(self):
        """Finds books by an author."""


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
    print("Welcome to Library Data Automation3")
    menu = Menu(authors_manager)

    # Display the main menu
    menu.display_menu()


main()
