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
        """
        self.sheet.update_cell(row, col, value)

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
        #Use the dictionary to have the feature to quickly change column's position
        self.atrubites_col = {"id": "ID", "full_name": "FULL NAME", "birth_year": "BIRTH YEAR"}
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
                record[self.atrubites_col["id"]],
                record[self.atrubites_col["full_name"]],
                record[self.atrubites_col["birth_year"]],
            )
            for record in records
        ]

    def check_duplicate_data(self, full_name, birth_year):
        """
        Checks the database for duplicate data by full name and birth year.

        Returns:
            ID if it is or None if it is not.
        """
        records = self.get_all_records()
        for record in records:
            if (
                record[self.atrubites_col["full_name"]] == full_name
                and record[self.atrubites_col["birth_year"]] == birth_year
            ):
                return record[self.atrubites_col["id"]]
        return None


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
            
            birth_year = None
            while True:
                try:
                    birth_year = input(
                    "Enter the birth year or 'Exit' to back to the previous step: "
                    )
                    if birth_year.lower() != "exit":
                        birth_year = int(birth_year)
                    
                    break
                
                except ValueError as e:
                    print(f"Invalid data: {e}, please try again.\n")
                
                
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
    print("Welcome to Library Data Automation")
    menu = Menu(authors_manager)

    # Display the main menu
    menu.display_menu()


main()
