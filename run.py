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
                "https://www.googleapis.com/auth/drive"
            ]
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
    
def main():
    """
    Run all program functions
    """
    sheet_name = 'library'
    worksheet_name = 'authors'
    # Initialize the client and open the worksheet
    client = GoogleSheetsClient(CREDS)
    worksheet = client.open_worksheet(sheet_name, worksheet_name)
    # Initialize the GoogleSheet class with the worksheet object
    google_sheet = GoogleSheet(worksheet)
    # Get all records
    print(google_sheet.get_all_records())
    # Get specific row
    print(google_sheet.get_row(2))
    # Update a cell
    google_sheet.update_cell(2, 2, 'New Value')
    # Append a new row
    google_sheet.append_row(['Value1', 'Value2', 'Value3'])
    # Find a value in a specific column
    cell = google_sheet.find_in_column(2, 'Value2')
    if cell:
        print(f"Found value at row {cell.row}, column {cell.col}")
    else:
        print("Value not found")

main()