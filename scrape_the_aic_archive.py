import os

import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def build_all_sector_csv(output_file_path: str, sectors: set[str]):
    for sector in sectors:
        # URL of the webpage
        # url = "https://www.theaic.co.uk/aic/find-compare-investment-companies?sortid=Name&desc=false"  # unfiltered
        url = f"https://www.theaic.co.uk/aic/find-compare-investment-companies?sec={sector}&sortid=Name&desc=false"  # sector specific

        # Initialize the WebDriver (ensure you have the correct WebDriver installed)
        driver = webdriver.Chrome()  # or another browser driver
        driver.get(url)

        # Wait until the table is loaded
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'table[role="table"]'))
            )
        finally:
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

        # Find the table
        table = soup.find('table', {'role': 'table'})

        # Check if the table is found
        if table:
            # Extract headers
            headers = [header.text.strip() for header in table.find_all('th')]

            # Extract rows
            rows = table.find_all('tr')[1:]  # Skip the header row
            data = []
            for row in rows:
                cells = row.find_all('td')
                cell_data = [cell.text.strip() for cell in cells]
                if any(cell_data):  # Only add rows with non-empty cells
                    data.append(cell_data)

            clean_headers = [header for header in headers
                             if (header != '') & (header != 'Share price total return (%)')]

            # print(headers)
            # print(len(headers))
            # print(clean_headers)
            # print(len(clean_headers))
            # print(data)
            # print(len(data[1]))

            # Create DataFrame
            df = pd.DataFrame(data, columns=clean_headers)

            # Initialize the new field record_type with default value 'Investment Trust'
            df['Record Type'] = 'Investment Trust'

            # Set the value to 'Sector' for the first record
            df.at[0, 'Record Type'] = 'Sector'

            # add sector and source
            df['Sector'] = sector
            df['Source'] = url

            # Save to CSV
            # Use mode='a' to append data to the file
            # Set header=False for subsequent appends to prevent writing headers again
            if os.path.exists(output_file_path):
                df.to_csv(output_file_path, index=False, mode="a", header=False)
            else:
                df.to_csv(output_file_path, index=False, mode="a")
            # print(df)
        else:
            print("Table not found")

    full_df = pd.read_csv(output_file_path)
    return full_df


def build_sector_aggregation_csv(input_file_path: str, output_file_path: str):
    full_df = pd.read_csv(input_file_path)
    # print(full_df)

    # manually calculate 10yr average for Technology & Technology Innovation (TCM) sector
    tcm_df = full_df[(full_df['Sector'] == 'TCM') & (full_df['Record Type'] == 'Investment Trust')].copy()

    # Convert values to numeric, non-numeric values become NaN
    tcm_df['10yr_num'] = pd.to_numeric(tcm_df['10yr'], errors='coerce')

    # Compute the average only for numeric values
    avg_value = tcm_df['10yr_num'].mean()
    # print(avg_value)

    # Replace a specific value with another value based on a condition
    condition = ((full_df['Sector'] == 'TCM')
                 & (full_df['Record Type'] == 'Sector')
                 & (full_df['10yr'] == '-')  # only if agg value not present
                 )  # TCM aggregate row

    full_df.loc[condition, '10yr'] = avg_value

    # get df which is filtered on just sector view
    df = full_df[full_df['Record Type'] == 'Sector'].copy()

    # Replace '-' with NaN and convert to float
    df['1yr'] = df['1yr'].apply(lambda x: float(x) if x != '-' else np.nan)
    df['5yr'] = df['5yr'].apply(lambda x: float(x) if x != '-' else np.nan)
    df['10yr'] = df['10yr'].apply(lambda x: float(x) if x != '-' else np.nan)

    # Calculate the ranks of values in 'col1' in descending order
    df['rank_1yr'] = df['1yr'].rank(ascending=False)
    df['rank_5yr'] = df['5yr'].rank(ascending=False)
    df['rank_10yr'] = df['10yr'].rank(ascending=False)

    # Create a new field 'top_5' to flag the top 5 values
    # 1yr flag
    df['top_5_1yr'] = 0  # Initialize all values to 0
    df.loc[df['rank_1yr'] <= 5, 'top_5_1yr'] = 1  # Set top 5 ranks to 1
    # 5yr flag
    df['top_5_5yr'] = 0  # Initialize all values to 0
    df.loc[df['rank_5yr'] <= 5, 'top_5_5yr'] = 1  # Set top 5 ranks to 1
    # 10yr flag
    df['top_5_10yr'] = 0  # Initialize all values to 0
    df.loc[df['rank_10yr'] <= 5, 'top_5_10yr'] = 1  # Set top 5 ranks to 1

    # print(df.columns)
    # print(df)
    # print(df.describe())

    # df.to_csv(output_file_path, index=False, mode="w")
    print(df.columns)
    # Merge the ranking back into the original DataFrame
    full_df = full_df.merge(df[['Company', 'Record Type', 'rank_1yr', 'rank_5yr', 'rank_10yr', 'top_5_1yr',
       'top_5_5yr', 'top_5_10yr']], on=['Company', 'Record Type'], how='left')
    print(full_df)

    full_df.to_csv(f'merged_{input_file_path}', index=False, mode="w")

    return df

