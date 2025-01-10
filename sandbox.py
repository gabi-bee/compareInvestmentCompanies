import pandas as pd

from scrape_the_aic import build_sector_aggregation_csv

pd.set_option('display.max_columns', None)

# Save to CSV with timestamp in filename
filename_all_sector = "aic_investment_companies__all_sector__20240520_214836.csv"
filename_sector_agg = "aic_investment_companies_20240520_214836__sector_agg__.csv"
# filename_all_sector = "aic_investment_companies_20240520_210708.csv"
# filename_sector_agg = "aic_investment_companies_20240520_210708__sector_agg__.csv"

df = build_sector_aggregation_csv(input_file_path=filename_all_sector, output_file_path=filename_sector_agg)

# Get unique values of 'col1' and sort them in descending order
# print(sorted(df['1yr'].unique(), reverse=True))
# print(sorted(df['5yr'].unique(), reverse=True))
# print(sorted(df['10yr'].unique(), reverse=True))

# selected_rows = df[df['top_5_1yr'] == 1]['Company', '1yr', 'rank_1yr', 'top_5_1yr']].sort_values('10yr', ascending=False)
# selected_rows = df[df['top_5_5yr'] == 1]['Company', '5yr', 'rank_5yr', 'top_5_5yr']].sort_values('10yr', ascending=False)
selected_rows = df[df['top_5_10yr'] == 1][['Company', '10yr', 'rank_10yr', 'top_5_10yr']].sort_values('10yr', ascending=False)
# selected_rows = df[df['10yr'] > 150]

# print(selected_rows)
#
# print(df[df['Company'] == 'Technology & Technology Innovation'][
#           ['Company', '1yr', '5yr', '10yr',
#            'Sector', 'Record Type',
#            'rank_1yr', 'rank_5yr', 'rank_10yr',
#            'top_5_1yr', 'top_5_5yr', 'top_5_10yr']])
#
# print(df[df['Sector'] == 'TCM'][
#           ['Company', '1yr', '5yr', '10yr',
#            'Sector', 'Record Type',
#            'rank_1yr', 'rank_5yr', 'rank_10yr',
#            'top_5_1yr', 'top_5_5yr', 'top_5_10yr']])