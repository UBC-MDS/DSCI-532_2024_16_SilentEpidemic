import pandas as pd


overall_df = pd.read_parquet('data/processed/overall.parquet')
specific_df = pd.read_parquet('data/processed/specific.parquet')
demo_df = pd.read_parquet('data/processed/demo.parquet')


def get_main_df():
    result = specific_df[specific_df['Opioid Type'] == 'overall']
    result['Year'] = pd.to_datetime(result['Year'], format='%Y')
    return result


main_df = get_main_df()


def get_opioid_df():
    result = specific_df[
        (specific_df["Drug Type"].isin(['Stimulants', 'Cocaine', 'Psychostimulants',
                                        'Benzodiazepines', 'Antidepressants'])) &
        (specific_df['Opioid Type'] == 'any')]
    result['Year'] = pd.to_datetime(result['Year'], format='%Y')
    return result

opioid_df = get_opioid_df()
