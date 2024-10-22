# FPI Sector Investment Data Extractor

This Python script retrieves the recent fortnightly Foreign Portfolio Investment (FPI) sector investment data from the provided URL and filters specific columns. The resulting data is saved into an Excel file in a specified naming convention.

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `pandas`
  - `openpyxl` (for saving Excel files)

You can install the required libraries using pip:

```bash
pip install requests pandas openpyxl
```

## Usage

To run the script, use the following command in your terminal:

```bash
python script.py <URL>
```

### Example

```bash
python script.py https://www.fpi.nsdl.co.in/web/StaticReports/Fortnightly_Sector_wise_FII_Investment_Data/FIIInvestSector_Sep302024.html
```

### Output

The output file will be named according to the following convention:

```
filtered_columns_FIIInvestSector_<Month><Day><Year>.xlsx
```

For example, if the URL corresponds to the fortnightly data for September 30, 2024, the output will be:

```
filtered_columns_FIIInvestSector_Sep302024.xlsx
```

### Script Details

1. **Fetching HTML Content**: The script fetches the HTML content of the specified URL using the `requests` library.
   
2. **Extracting Data**: It extracts the first table from the HTML content using `pandas`.

3. **Filtering Columns**: The script filters the following columns by their indices:
   - Column 1 - Sectors 
   - Column 26 - Equity under Net Investment example - September 01-15, 2024
   - Column 50 - Equity under Net Investment example - September 16-30, 2024

4. **Saving to Excel**: The filtered data is saved to an Excel file with the specified naming convention.

### Note

- Ensure that the URL provided points to a valid webpage containing the desired data.
- The script is designed to work with the structure of the specific FPI sector investment data webpage.
