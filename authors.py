from colorama import Fore
from googlesheets_setup import GoogleSheetsClient, GoogleSheet
from mixin_classes import UniqueIDMixin, InputMixin


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
        # Use the dictionary to have the feature to quickly change a column's
        # position
        self.attributes_name = {
            "id": "ID",
            "full_name": "FULL NAME",
            "birth_year": "BIRTH YEAR",
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
            self.attributes_name["full_name"],
            self.attributes_name["birth_year"]
        ]

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
            lambda i, values_row: (
                f'{i}. {values_row[self.attributes_name["id"]]} - '
                f'{values_row[self.attributes_name["full_name"]]} - '
                f'{values_row[self.attributes_name["birth_year"]]}'
            )
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
            # If no author is found, set the author to None
            author = values_row
        else:
            # If an author is found, create an Author object with
            # the retrieved data
            author = Author(
                values_row[self.attributes_name["id"]],
                values_row[self.attributes_name["full_name"]],
                values_row[self.attributes_name["birth_year"]],
            )

        if author:
            # If an author was found, print the author's details in green
            print(Fore.GREEN + f"The author is {author.to_fstring()}")

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
