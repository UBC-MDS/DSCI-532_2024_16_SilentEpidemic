import os
import pandas as pd
from parse_config import config, overall_columns, specific_columns, demographic_columns


RAW_DATA_FILE = "./data/raw/Overdose_data_1999-2021 1.19.23.xlsx"
OUTPUT_DIR = "./data/processed/"


def read_raw_data():
    """Reads in raw data.

    Returns
    -------
    dict
        A dictionary that contain pandas data frames.
        The data frames contain the raw data with non-relevant rows and columns dropped.

    """
    raw_dfs = {}
    for k, v in config.items():
        raw_dfs[k] = pd.read_excel(RAW_DATA_FILE, sheet_name=k, skiprows=6)
        raw_dfs[k] = raw_dfs[k].drop(columns=['Unnamed: 0'], axis=1)
        raw_dfs[k].set_index('Unnamed: 1', inplace=True)
        raw_dfs[k] = raw_dfs[k].iloc[0:v['valid_rows']].loc[:, 1999:2021]
    return raw_dfs


def get_deaths_and_rate(raw_dfs, num_df_name, rate_df_name, pop_type):
    """Parse and convert the data into a long format.

    Parameters
    ----------
    raw_dfs
        Dictionary returned from read_raw_data().

    num_df_name
        Name of the Excel Spreadsheet that contains the number of deaths.

    rate_df_name
        Name of the Excel Spreadsheet that contains the death rates.

    pop_type
        Name of the population (i.e. "Overall"/"Young Adult")

    Returns
    -------
    (list, list)
        Two lists containing deaths, death rates and other relevant attributes.
        The first list contains the overall figures for each year, while the second list
        contains figures from specific drug types and other relevant attributes.

    """
    overall_rows = []
    specific_rows = []

    for year in range(1999, 2022):
        for attributes, idx in config[num_df_name]['indices'].items():
            deaths = raw_dfs[num_df_name].loc[:, year].iloc[idx]
            rate = raw_dfs[rate_df_name].loc[:, year].iloc[idx]
            if len(attributes) == 2:
                overall_rows.append([*attributes, deaths, rate, year, pop_type])
            else:
                specific_rows.append([*attributes, deaths, rate, year, pop_type])

    return overall_rows, specific_rows


def preprocess():
    """Preprocess the raw data.
    """
    raw_dfs = read_raw_data()

    # handle overall data
    o1, s1 = get_deaths_and_rate(raw_dfs,'Number Drug OD Deaths',
                                 'Rate Drug OD Deaths',"Overall")

    # handle young adult data
    o2, s2 = get_deaths_and_rate(raw_dfs, 'Number Drug OD, 15-24 Years',
                                 'Rate Drug OD, 15-24 Years', "Young Adults, 15-24 Years")

    overall_rows = o1 + o2
    specific_rows = s1 + s2

    # TODO: handle demographic data

    overall_df = pd.DataFrame(overall_rows, columns=overall_columns)
    specific_df = pd.DataFrame(specific_rows, columns=specific_columns)

    overall_df.to_csv(os.path.join(OUTPUT_DIR, "overall.csv"))
    specific_df.to_csv(os.path.join(OUTPUT_DIR, "specific.csv"))


if __name__ == "__main__":
    preprocess()
