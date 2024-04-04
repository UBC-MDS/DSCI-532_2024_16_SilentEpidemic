"""
This script processes overdose data from an Excel file. It includes functions to:

1. Read and preprocess the data.
2. Rename columns based on gender and drug type.
3. Append a suffix to column names.

The script then uses these functions to process data in every sheet, rename the gender columns, and export the processed data to a CSV file.
"""

import pandas as pd

def process_overdose_data(sheet_name):
    """
    This function reads an Excel file of overdose data, processes it, and returns a transposed DataFrame.
    
    Parameters:
    sheet_name (str): The name of the sheet in the Excel file to read.
    
    Returns:
    df_processed (DataFrame): The processed DataFrame.
    """
    # Read the Excel file
    df_load = pd.read_excel('../data/raw/Overdose_data_1999-2021 1.19.23.xlsx', sheet_name=sheet_name, skiprows=6)
    # Drop the first column
    df_load = df_load.drop(df_load.columns[0], axis=1)
    # Set the index using the first column
    df_load.set_index(df_load.columns[0], inplace=True)
    # Transpose the DataFrame
    df_processed = df_load.T
    # Remove leading spaces from column names
    df_processed.columns = df_processed.columns.str.strip()
    # Drop columns where all values are NaN
    df_processed = df_processed.dropna(axis=1, how='all')
    
    return df_processed

def rename_columns(df):
    """
    This function renames the columns of a DataFrame by prepending the drug type to 'Female' and 'Male'.
    
    Parameters:
    df (DataFrame): The DataFrame to rename the columns of.
    
    Returns:
    df (DataFrame): The DataFrame with renamed columns.
    """
    new_columns = []
    for i in range(len(df.columns)):
        if df.columns[i] == 'Female':
            drug_type = df.columns[i - 1]
            new_columns.append(f"{drug_type} {df.columns[i]}")
        elif df.columns[i] == 'Male':
            drug_type = df.columns[i - 2]
            new_columns.append(f"{drug_type} {df.columns[i]}")
        else:
            new_columns.append(df.columns[i])
    df.columns = new_columns
    return df

def append_suffix(df, suffix):
    """
    This function appends a suffix to each column name in a DataFrame.
    
    Parameters:
    df (DataFrame): The DataFrame to append the suffix to the columns of.
    suffix (str): The suffix to append to each column name.
    
    Returns:
    df (DataFrame): The DataFrame with the modified column names.
    """
    df.columns = [f"{col}_{suffix}" for col in df.columns]
    return df

# process overall no. of death
sheet_name = 'Number Drug OD Deaths'
df_od_death = process_overdose_data(sheet_name)
df_od_death = rename_columns(df_od_death)

# process no. of death for 15-24 yo
sheet_name = 'Number Drug OD, 15-24 Years'
df_od_death_youth = process_overdose_data(sheet_name)
df_od_death_youth = rename_columns( df_od_death_youth)
df_od_death_youth = append_suffix(df_od_death_youth, 'youth')

# combine the no. of death
df_od_death_all = pd.concat([df_od_death, df_od_death_youth], axis=1)

# process overall rate of OD death
sheet_name = 'Rate Drug OD Deaths'
df_od_rate = process_overdose_data(sheet_name)
df_od_rate = rename_columns(df_od_rate)

# process rate of death for 15-24 yo
sheet_name = 'Rate Drug OD, 15-24 Years'
df_od_rate_youth = process_overdose_data(sheet_name)
df_od_rate_youth = rename_columns( df_od_rate_youth)
df_od_rate_youth = append_suffix(df_od_rate_youth, 'youth')

# combine the rate of death
df_od_rate_all = pd.concat([df_od_rate, df_od_rate_youth ], axis=1)

# process demographic rate
sheet_name = 'Rate OD by Demographic'
df_rate_demo = process_overdose_data(sheet_name)
df_rate_demo = rename_columns(df_rate_demo)
df_rate_demo.columns.values[3:21] = ['total ' + col for col in df_rate_demo.columns[3:21]]

def rename_race_columns(df):
    """
    This function renames the race columns of a DataFrame by prepending the drug type to each race category.
    
    Parameters:
    df (DataFrame): The DataFrame to rename the columns of.
    
    Returns:
    df (DataFrame): The DataFrame with renamed columns.
    """
    new_columns = []
    for i in range(len(df.columns)):
        if df.columns[i] == 'White (Non-Hispanic)':
            drug_type = df.columns[i - 3]
            new_columns.append(f"{drug_type} {df.columns[i]}")
        elif df.columns[i] == 'Black (Non-Hispanic)':
            drug_type = df.columns[i - 4]
            new_columns.append(f"{drug_type} {df.columns[i]}")
        elif df.columns[i] == 'Asian* (Non-Hispanic)':
            drug_type = df.columns[i - 5]
            new_columns.append(f"{drug_type} {df.columns[i]}")
        elif df.columns[i] == 'Native Hawaiian or Other Pacific Islander* (Non-Hispanic)':
            drug_type = df.columns[i - 6]
            new_columns.append(f"{drug_type} {df.columns[i]}")
        elif df.columns[i] == 'Hispanic':
            drug_type = df.columns[i - 7]
            new_columns.append(f"{drug_type} {df.columns[i]}")
        elif df.columns[i] == 'American Indian or Alaska Native (Non-Hispanic)':
            drug_type = df.columns[i - 8]
            new_columns.append(f"{drug_type} {df.columns[i]}")
        else:
            new_columns.append(df.columns[i])
    df.columns = new_columns
    return df

df_rate_demo = rename_race_columns(df_rate_demo)

# export to csv files
df_od_death_all.to_csv('../data/processed/od_deathnumber.csv')
df_od_rate_all.to_csv('../data/processed/od_deathrate.csv')
df_rate_demo.to_csv('../data/processed/od_rate_demo.csv')
