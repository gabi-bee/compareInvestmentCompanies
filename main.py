from datetime import datetime

import pandas as pd

from scrape_the_aic import build_all_sector_csv, build_sector_aggregation_csv

pd.set_option('display.max_columns', None)

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def run_all():

    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save to CSV with timestamp in filename
    filename_all_sector = f'aic_investment_companies_{timestamp}.csv'
    filename_sector_agg = f'aic_investment_companies_{timestamp}__sector_agg__.csv'

    sector_list = [
        "ASP",  # Asia Pacific
        "ASI",
        "ASS",
        "BIO",
        "CHN",
        "CNR",
        "CSP",
        "DDL",
        "DLB",
        "DSF",
        "ENV",
        "EUR",
        "ESC",
        "TIM",
        "FIN",
        "FLX",
        "GG",
        "GEM",
        "GGI",
        "GSC",
        "GCP",
        "HDG",
        "IND",
        "INF",
        "UTL",
        "INS",
        "JPN",
        "JSC",
        "LAM",
        "LEA",
        "NA",
        "NAS",
        "PE",
        "PRD",
        "PRE",
        "PRW",
        "PUC",
        "PUH",
        "PUL",
        "PUR",
        "PPS",
        "REI",
        "ROY",
        "TCM",
        "UGR",
        "UKH",
        "UGI",
        "USC",
        "VCA",
        "VCG",
        "VGP",
        "VCE",
        "VCH",
        "VPT",
        "VTP",
    ]
    sector_keys = set(sector_list)  # get unique list

    full_df = build_all_sector_csv(output_file_path=filename_all_sector, sectors=sector_keys)
    # print(full_df)

    build_sector_aggregation_csv(input_file_path=filename_all_sector, output_file_path=filename_sector_agg)


if __name__ == '__main__':
    run_all()
