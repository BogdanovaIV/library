from googlesheets import GoogleSheetsClient, GoogleSheet
from mixin_classes import UniqueIDMixin, InputMixin
from colorama import Fore


class Book:
    """
    Represents a book.

    Attributes:
        id (str): The book's ID.
        title (str): The book's title.
        author_id (str): The author's ID.
        shelf_number (str): The number of the shelf on which the book is
        stored.
    """

    def __init__(self, id, title, author_id, shelf_number):
        """
        Initializes the Book class with the given details.

        Args:
            id (str): The book's ID.
            title (str): The book's title.
            author_id (str): The author's ID.
            shelf_number (str): The number of the shelf on which the book is
            stored.
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
        return (
            f"{self.id} - {self.title} - {author_full_name} - "
            f"shelf ({self.shelf_number})"
        )


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
        # Use the dictionary to have the feature to quickly change a column's
        # position
        self.attributes_name = {
            "id": "ID",
            "title": "TITLE",
            "author_id": "AUTHOR (ID)",
            "shelf_number": "SHELF",
        }

        super().__init__(sheet)

    def get_headers_for_table(self):
        """
        Return headers of columns for the table

        Returns:
            list: A list of headers.
        """

        return [
            self.attributes_name["id"],
            self.attributes_name["title"],
            "AUTHOR",
            self.attributes_name["shelf_number"]
        ]

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
            attributes_any (dict): A dictionary where the key is an attribute
            and the value is the value being tested. To match though one of
            them has to be equal.
            attributes_all (dict): A dictionary where the key is an attribute
            and the value is the value being tested. To match all of them have
            to be equal.

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
            lambda i, values_row: (
                f'{i}. {values_row[self.attributes_name["id"]]} - '
                f'{values_row[self.attributes_name["title"]]}'
            )
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
            print(
                Fore.GREEN +
                f"The book is {book.to_fstring(author_full_name)}"
            )
        return (
            book,
            index,
        )
