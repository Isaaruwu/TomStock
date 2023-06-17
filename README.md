# TomStock

This scheduled script is designed to retrieve stock data using the yfinance library and write it into a Google Spreadsheet using the Google Sheets API. The script also help with spreadsheet maintenance by removing unused tabs. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required Python packages.

```bash
pip install -r requirements.txt
```

## Project Setup

1. Follow the guide on the Google Sheets API documentation to create a GCP project
2. Enable the Google Sheets API
3. Generate the required credentials file
4. Rename the credentials file to keys.json and place it in the project's root directory.

5. Open the Google Spreadsheet where you want to write the stock data. Copy the spreadsheet's ID from the URL and store it in a sp_id.txt file in the project's root directory.
6. Create a sheet named config and write the tickers of the stocks to track in column A
