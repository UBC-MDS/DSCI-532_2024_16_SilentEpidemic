import plotly.express as px

DRUG_OPIOIDS = {'Prescription opioids', 'Synthetic opioids', 'Heroin'}

# For plot colour formatting (opioid.py and deaths.py)
unique_drug_types=['Antidepressants', 'Benzodiazepines', 'Cocaine', 'Heroin', 'Prescription opioids', 'Psychostimulants', 'Stimulants', 'Synthetic opioids']
prism_colors = px.colors.qualitative.Prism
drug_color_mapping = dict(zip(unique_drug_types, prism_colors))
color_sequence = [drug_color_mapping[drug_type] for drug_type in unique_drug_types]

# For plot colour formatting (demo.py)
unique_demos = ['Overall', 'American Indian or Alaska Native (Non-Hispanic)', 'Asian (Non-Hispanic)', 'Black (Non-Hispanic)', 'Hispanic', 'Native Hawaiin or Other Pacific Islander (Non-Hispanic)', 'White (Non-Hispanic)']
demo_color_mapping = dict(zip(unique_demos, prism_colors))
demo_color_sequence = [demo_color_mapping[demo] for demo in unique_demos]
