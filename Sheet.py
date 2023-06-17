from googleapiclient.discovery import Resource


class Sheet:
    """A class for interacting with a google spreadsheet

    This class provides methods to read, write, and manipulate data in a sheet

    Args & Attributes:
        sheet (Resource): The Sheet resource object
        sheet_id (str): The ID of the sheet
    """

    def __init__(self, sheet: Resource, sheet_id: str):
        """Initialize a Sheet object

        Args:
            sheet (Resource): The Sheet resource object.
            sheet_id (str): The ID of the sheet.
        """
        self.sheet = sheet
        self.sheet_id = sheet_id
        self.config = self.read_sheet("config!A:A")

    def get_config(self) -> list:
        """Get the stocks in the config sheet
        Returns:
                list: Stocks in the config sheet
        """
        print(self.config)
        return [stock[0] for stock in self.config if stock]

    def read_sheet(self, sheet_range: str) -> list:
        """Read data from a sheet
        Args:
                sheet_range (str): Cell range to read

        Returns:
                list: Cells values in the given range
        """
        result = (
            self.sheet.values()
            .get(spreadsheetId=self.sheet_id, range=sheet_range)
            .execute()
        )
        return result.get("values", [])

    def get_stock_tabs(self) -> list[str]:
        """Get the names of the stock tabs

        Returns:
                list: Names of the stock tabs excluding the first 4 tabs
        """
        request = self.sheet.get(
            spreadsheetId=self.sheet_id, fields="sheets(properties(sheetId,title))"
        ).execute()
        return [tab["properties"]["title"] for tab in request["sheets"]][4:]

    def write_sheet(self, sheet_range: str, data: list) -> None:
        """Writes data to a sheet
        Args:
                sheet_range (str): Cell range to read
                data (list): Data to write
        """
        self.sheet.values().update(
            spreadsheetId=self.sheet_id,
            range=sheet_range,
            valueInputOption="USER_ENTERED",
            body={"values": data},
        ).execute()

    def add_sheet(self, sheet_name: str) -> None:
        """Adds a new sheet to the spreadsheet
        Args:
                sheet_name (str): Name of the new sheet
        """
        self.sheet.batchUpdate(
            spreadsheetId=self.sheet_id,
            body={"requests": [{"addSheet": {"properties": {"title": sheet_name}}}]},
        ).execute()

    def delete_sheet(self, sub_sheet_id: str) -> None:
        """Deletes a sheet from the spreadsheet
        Args:
                sheet_name (str): Name of the new sheet
        """
        self.sheet.batchUpdate(
            spreadsheetId=self.sheet_id,
            body={"requests": [{"deleteSheet": {"sheetId": sub_sheet_id}}]},
        ).execute()

    def clean_spreadsheet(self) -> None:
        """Removes sheets that are not in the configuration"""
        tabs = self.get_stock_tabs()
        config = self.get_config()
        all_sheet = (
            self.sheet.get(spreadsheetId=self.sheet_id).execute().get("sheets", "")
        )

        for stock in tabs:
            if stock not in config:
                sheets = [
                    sheet
                    for sheet in all_sheet
                    if sheet.get("properties", {}).get("title", "Sheet1") == stock
                ]
                sub_sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)
                self.delete_sheet(sub_sheet_id)
