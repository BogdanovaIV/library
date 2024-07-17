import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore


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
            creds (google.oauth2.service_account.Credentials):
            The credentials for authentication.
        """
        self.client = self.authenticate(creds)

    @staticmethod
    def get_creds(creds_file):
        """
        Generates credentials from the service account file.

        Args:
            creds_file (str): Path to the credentials JSON file.

        Returns:
            google.oauth2.service_account.Credentials:
            The generated credentials.
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
            creds (google.oauth2.service_account.Credentials):
            The credentials for authentication.

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
            self.sheet.update(
                range_name=f"A{row}:Z{row}",
                values=[values_list]
                              )
            print(Fore.GREEN + "Row updated successfully.")
            return True
        except Exception as e:
            print(Fore.RED + f"Failed to update row: {e}")
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
            print(Fore.GREEN + "Row appended successfully.")
            return True
        except gspread.exceptions.APIError as e:
            print(Fore.RED + f"Failed to append row: {e}")
            return False

    def find_cells_contain_value(self, attributes_any, attributes_all):
        """
        Finds all cells that match a specific value in the worksheet.

        Args:
            attributes_any (dict): A dictionary where the key is an attribute
            and the value is the value being tested. To match though one of
            them has to be equal.
            attributes_all (dict): A dictionary where the key is an attribute
            and the value is the value being tested.To match all of them have
            to be equal.

        Returns:
            list: A list of gspread.models.Cell objects that match the value.
        """
        records = self.sheet.get_all_records()
        matching_records = []
        for row, record in enumerate(records, start=2):
            if (not attributes_any or any(
                value.lower() in record.get(attr).lower()
                for attr, value in attributes_any.items()
            )) and all(
                value.lower() in record.get(attr).lower()
                for attr, value in attributes_all.items()
            ):
                matching_records.append([row, record])
        return matching_records

    def find_item(
        self,
        attributes_any,
        attributes_all,
        text_item,
        print_item_lambda
    ):
        """
        Find an item by values that have to be equal.

        Args:
            attributes_any (dict): A dictionary where the key is an attribute
            and the value is the value being tested. To match though one of
            them has to be equal.
            attributes_all (dict): A dictionary where the key is an attribute
            and the value is the value being tested. To match all of them have
            to be equal.
            text_item (str): String of the name of the item to print to
            the user.
            print_item_lambda (lambda): Lambda function which prints
            the detailed information of the item

        Returns:
            Dictionary: The found item which contains details.
            int: The row number where the item was found.
            or
            None: If no item was found.
            int: -1 if no item was found.
        """

        cells = self.find_cells_contain_value(attributes_any, attributes_all)

        if not cells:
            print(Fore.RED + f"The {text_item} is not found.\n")
            return None, -1

        if len(cells) == 1:
            index = 0
        else:
            index = self.choose_item(cells, text_item, print_item_lambda)

        values_row = cells[index][1]
        return (
            values_row,
            cells[index][0],
        )

    def choose_item(self, cells, text_item, print_item_lambda):
        """
        Prompts the user to choose an item from multiple matches.

        Args:
            cells (list): List of matched cells.
            text_item (str): String of the name of the item to print to
            the user.
            print_item_lambda (lambda): Lambda function which prints
            the detailed information of the item.
                The function has to have two arguments:
                i (integer) - The row number where the item was found.
                values_row (dict) - The item which contains details.

        Returns:
            int: The index of the chosen item.
        """
        while True:
            print(f"Choose the {text_item}:")
            for i, cell in enumerate(cells, start=1):
                values_row = cell[1]
                print(print_item_lambda(i, values_row))
            try:
                choice = int(input("Enter your choice:\n"))
                if 0 < choice <= len(cells):
                    return choice - 1

                raise ValueError(Fore.RED + "Please enter a valid option.")
            except ValueError as e:
                print(Fore.RED + f"Invalid data: {e}, please try again.\n")

    def check_duplicate_data(self, attributes):
        """
        Checks the database for duplicate data by specified attributes.

        Args:
            attributes (dict): A dictionary where the key is an attribute and
            the value is the value being tested.

        Returns:
            Dictionary: The record if a duplicate is found, otherwise None.
        """
        records = self.get_all_records()
        for record in records:
            if all(
                record.get(attr) == value for attr,
                value in attributes.items()
            ):
                return record
        return None
