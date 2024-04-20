import pandas as pd


overall_df = pd.read_parquet('data/processed/overall.parquet')
specific_df = pd.read_parquet('data/processed/specific.parquet')
demo_df = pd.read_parquet('data/processed/demo.parquet')
