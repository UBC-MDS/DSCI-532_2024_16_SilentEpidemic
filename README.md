# The Slient Epidemic: National Drug Overdose Deaths
Dash dashboard visualizing America's drug overdose death rates. The dashboard can be found [here](https://dsci-532-2024-16-silentepidemic.onrender.com/)).

## Dashboard Contents:

### Problem & Importance
Dr. Darling and our group are concerned about the alarming rise in national drug overdose deaths and want to provide additional education for upper high school students. This issue is of significant concern due to several factors:
1. Increasing Overdose Deaths: Overdose deaths, especially those involving synthetic opioids like fentanyl, have increased significantly in recent years. This trend is not only concerning but also indicative of a larger, systemic issue that needs to be addressed.
2. Unintentional Overdoses: Many overdoses are unintentional, often occurring because individuals underestimate the dangers of mixing drugs or are unaware of the potency of the substances they are using. This lack of awareness and understanding significantly contributes to the high rates of overdose deaths.
3. Need for Education: There is a critical need for effective education programs that can equip students with the knowledge and skills to identify the risks of different drugs and recognize the signs and symptoms of overdose. Such education is crucial in preventing drug misuse and potentially saving lives.
4. Target Demographic: The target demographic for this education is upper high school students. This group is particularly important as they are at an age where they may be exposed to drugs and are at risk of drug misuse. By providing them with the necessary knowledge and understanding, we can empower them to make informed decisions and reduce the risk of drug overdose.

### How Our Dashboard Helps
The SilentEpidemic dashboard was created as a teaching tool for high school students in California. It is intended to raise awareness for the increasing rate of drug overdose deaths within the general population and within the 15-24 age group. The dashboard highlights the discrepancies in drug overdose deaths by ethnicity and gender, and also shows the rise in opioid-related deaths over time. 

Our dashboard visualizes:
*** Add GIF here ***
- Overdose Trends: Shows a clear upward trend in national drug overdose deaths over time, particularly focusing on the rise in synthetic opioid-related deaths.
- Drug Risk Comparisons: Visually represents the relative risks associated with different drug categories, highlighting the dangers of synthetic opioids compared to other substances.
- Demographic Disparities: Highlights potential risk factors by ethnicity and gender to identify high-risk student populations.

## Usage

1. Try out the App! To start using the Silent Epidemic dashboard, click here: [Silent Epidemic Dashboard](https://dsci-532-2024-16-silentepidemic.onrender.com/).
On the dashboard, begin your exploration by selecting your demographic of interest, drug type, and year range. Use the Drug Type Filter if you’d like to focus on specific types of drugs. Dive in and observe the trends and patterns in overdose death rates across different demographics!

2. If you are interested in contributing to the development of the Silent Epidemic dashboard, please read the [contributing guidelines](https://github.com/UBC-MDS/DSCI-532_2024_16_SilentEpidemic/blob/main/CONTRIBUTING.md) for full details. Below are some quick steps to run the app locally.
- In your terminal run:
```bash
git clone git@github.com:UBC-MDS/DSCI-532_2024_16_SilentEpidemic.git
cd DSCI-532_2024_16_SilentEpidemic
```
- Create and activate the virtual environment
In the root of the repository run:
```bash 
virtualenv ./venv
source ./venv/bin/activate
```
- Create a branch for local development and make your changes
```bash 
git checkout -b name-of-your-fix-or-feature
```
- To run the dashboard
```bash 
python src/app.py
```

## Contributors: 
The SilentEpidemic dashboard was created by Orix Au Yeung (@SoloSynth1), Yingzi Jin (@jinyz8888), Alysen Townsley (@AlysenTownsley), Bill Wan(@billwan96)

## Contributing:
Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License: 
The SilentEpidemic dashboard is licensed under the terms of the MIT license and [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/). Please refer to [the license file](LICENSE) for more information.

## References:
1. Dataset Reference: National Institute on Drug Abuse. (2023). Overdose Data 1999-2021 [Excel file]. Retrieved from https://nida.nih.gov/sites/default/files/Overdose_data_1999-2021%201.19.23.xlsx
