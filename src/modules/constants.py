import plotly.express as px

DRUG_OPIOIDS = {'Prescription opioids', 'Synthetic opioids', 'Heroin'}
UNIQUE_DRUG_TYPES = ('Antidepressants', 'Benzodiazepines', 'Cocaine', 'Heroin', 'Prescription opioids', 'Psychostimulants', 'Stimulants', 'Synthetic opioids')
UNIQUE_DEMOS = ('Overall', 'American Indian or Alaska Native (Non-Hispanic)', 'Asian (Non-Hispanic)', 'Black (Non-Hispanic)', 'Hispanic', 'Native Hawaiin or Other Pacific Islander (Non-Hispanic)', 'White (Non-Hispanic)')

REPO_NAME = "UBC-MDS/DSCI-532_2024_16_SilentEpidemic"
REPO_URL = f"https://github.com/{REPO_NAME}"
API_ENDPOINT = f"https://api.github.com/repos/{REPO_NAME}"

COLOR_SCHEME = px.colors.qualitative.Prism

# For plot colour formatting (opioid.py and deaths.py)
DRUG_COLOR_MAPPING = dict(zip(UNIQUE_DRUG_TYPES, COLOR_SCHEME))
COLOR_SEQUENCE = [DRUG_COLOR_MAPPING[drug_type] for drug_type in UNIQUE_DRUG_TYPES]

# For plot colour formatting (demo.py)
DEMO_COLOR_MAPPING = dict(zip(UNIQUE_DEMOS, COLOR_SCHEME))
DEMO_COLOR_SEQUENCE = [DEMO_COLOR_MAPPING[demo] for demo in UNIQUE_DEMOS]

