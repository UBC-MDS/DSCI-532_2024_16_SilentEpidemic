import pandas as pd


overall_df = pd.read_parquet('data/processed/overall.parquet')
specific_df = pd.read_parquet('data/processed/specific.parquet')
demo_df = pd.read_parquet('data/processed/demo.parquet')

opioid_df = specific_df[
    (specific_df["Drug Type"].isin(['Stimulants', 'Cocaine', 'Psychostimulants', 'Benzodiazepines', 'Antidepressants'])) &
    (specific_df['Opioid Type'] == 'any')
]