from googlesheets import GoogleSheetsClient
from authors import Authors
from books import Books
from menu import Menu


CREDS = GoogleSheetsClient.get_creds("creds.json")


def main():
    """Run all program functions"""
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
