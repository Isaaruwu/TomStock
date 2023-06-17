from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
import yfinance as yf
from Sheet import Sheet


def get_stock_data(stock: str, period: str, include_headers=True) -> list:
    """_summary_
    Args:
            stock (str): Ticker symbol of the stock
            period (str): Period of the stock data
            include_headers (bool, optional): Including Headers
            in the returned list. Defaults to True.

    Returns:
            lst: Formatted list of stock data
    """
    stock = yf.Ticker(stock.upper())
    try:
        stock_data = stock.history(period=period)
        stock_data.index = stock_data.index.strftime("%Y-%m-%d")
        data_list = stock_data.reset_index().values.tolist()
        headers = ["Date"] + stock_data.columns.tolist()
        data = [headers] + data_list
        return data if include_headers else data_list
    except:  # pylint: disable=W0702
        return []

def init_config(sheet: Sheet) -> None:
    """_summary_
    Reads the config sheet and creates new tabs for the stocks

    Args:
            sheet (Resource): Sheet object
            sheet_id (str): Sheet id
    """
    sheet.clean_spreadsheet()
    
    config = sheet.get_config()
    tabs = sheet.get_stock_tabs()

    for stock in config:
        if stock not in tabs:
            stock_data = get_stock_data(stock, "1mo")
            if stock_data:
                sheet.add_sheet(stock)
                sheet.write_sheet(stock + "!A1", stock_data)


def update_stock_daily(sheet: Sheet) -> None:
    """_summary_
    Updates the daily stock data

    Args:
            sheet (Resource): Sheet object
            sheet_id (str): Sheet id
    """
    tabs = sheet.get_stock_tabs()
    for tab in tabs:
        stock_data = get_stock_data(tab, "1d", include_headers=False)
        sheet_data = sheet.read_sheet(tab + "!A:A")
        prev_date = sheet_data[-1][0]
        data_date = stock_data[0][0]
        if stock_data and data_date != prev_date:
            position = len(sheet_data) + 1
            sheet.write_sheet(tab + f"!A{position}", stock_data)


if __name__ == "__main__":
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SERVICE_ACCOUNT_FILE = "keys.json"

    credentials = None
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    with open("sp_id.txt", "r", encoding="utf-8") as f:
        SP_ID = f.read().strip()

    service = build("sheets", "v4", credentials=credentials)
    sheet_obj = service.spreadsheets()

    sheet_inst = Sheet(sheet_obj, SP_ID)

    init_config(sheet_inst)
    update_stock_daily(sheet_inst)
