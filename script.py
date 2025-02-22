import sys
import requests
import pandas as pd
from urllib.parse import urlparse
import os

def fetch_html_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        sys.exit(1)

def extract_and_save_filtered_columns(html_content, output_file, target_indices):
    """Extract the first table from HTML content, filter specific columns, and save to a new Excel file."""
    try:
        tables = pd.read_html(html_content)

        if not tables:
            print("No tables found on the webpage.")
            return

        # Use the first table
        first_table = tables[0]

        # Check if the specified indices are within the column range
        max_index = first_table.shape[1] - 1  # Maximum valid column index
        invalid_indices = [idx for idx in target_indices if idx > max_index]
        if invalid_indices:
            print(f"Warning: These column indices are out of range: {invalid_indices}")

        # Extract columns by index, ignoring invalid ones
        valid_indices = [idx for idx in target_indices if idx <= max_index]
        filtered_df = first_table.iloc[:, valid_indices]

        # Create a Pandas Excel writer using XlsxWriter as the engine
        writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
        filtered_df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Get the workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Define the formats for positive and negative numbers
        green_format = workbook.add_format({'bg_color': '#00B050'})  # Light green
        red_format = workbook.add_format({'bg_color': '#FF0000'})    # Light red

        # Apply conditional formatting to columns 26 and 50 (B and C in Excel)
        for col_idx in [1, 2]:  # Excel columns B and C (0-based index)
            for row in range(1, len(filtered_df) + 1):  # Skip header row
                cell_value = filtered_df.iloc[row-1, col_idx]
                try:
                    # Try to convert to float and check if it's a number
                    value = float(str(cell_value).replace(',', ''))
                    if value > 0:
                        worksheet.write(row, col_idx, cell_value, green_format)
                    elif value < 0:
                        worksheet.write(row, col_idx, cell_value, red_format)
                except (ValueError, TypeError):
                    # If conversion fails, it's not a number, keep original formatting
                    worksheet.write(row, col_idx, cell_value)

        # Save the workbook
        writer.close()
        print(f"Filtered columns saved to {output_file} with color formatting.")
    except Exception as e:
        print(f"Error: {e}")

def generate_output_filename(url):
    """Generate the output filename based on the URL."""
    parsed_url = urlparse(url)
    # Extract the last part of the path and remove the .html extension
    base_name = parsed_url.path.split("/")[-1].replace(".html", "")
    # Save to output directory when running in Docker
    output_dir = "/app/output" if os.path.exists("/app") else "."
    output_file = os.path.join(output_dir, f"filtered_columns_{base_name}.xlsx")
    return output_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    html_content = fetch_html_content(url)

    # Generate the output filename based on the URL
    output_file = generate_output_filename(url)
    target_indices = [1, 26, 50]  # Target column indices

    extract_and_save_filtered_columns(html_content, output_file, target_indices)
