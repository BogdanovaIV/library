from googlesheets import GoogleSheetsClient
from authors import Authors
from books import Books
from menu import Menu
from colorama import Fore
import os


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

    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear') 

    # Create a Menu instance
    print(
        Fore.BLUE +
        f"Welcome to Library Data Automation!\n"
        f"This application stores information about authors and books. "
        f"It allows the user to get the list of authors and books, "
        f"add a new author and a new book, edit existing authors and books "
        f"and display books with a section by an author and a part of "
        f"the title."
    )
    menu = Menu(authors_manager, books_manager)

    # Display the main menu
    menu.display_menu()


if __name__ == "__main__":
    main()
