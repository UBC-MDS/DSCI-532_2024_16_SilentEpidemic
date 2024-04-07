# Implemented Features:
## Cards and plots, including:
- Cumulative Deaths from All Drugs: A widget that accumulates the total number of overdose deaths due to all drug typyes, all gender and all demographic.
- Average Death Rate: A card displays the weighted average death rate by multiplying each death rate by the number of deaths for that rate, summing these products, and then dividing by the total number of deaths.
- Percentage Young Adult Deaths: A card demontrates the percentage of deaths that occurred among young adults (15-24 years).
- Fold Change: This card shows the multiplicative increase or decrease in deaths over the selected time period.
- Overdose Deaths and Death Rates by Drug Type: A bubble chart shows the number of deaths by drug type, with size indicating volume and color representing the drug category.
- Percentage of Overdose Deaths Involving Opioids by Drug Type: A line chart tracking the percentage of overdoses involving opioids, among others, over time.
- Overdose Death Rate Based on Demographic: A bar chart breaking down overdose death rates by demographic categories.
## Interactive filters, including:
- Sex: A dropdown menu allows users to filter data by gender, with options like "All Sexes" or specific genders.
- Drug Type: A list of checkboxes for different drug categories such as "Any opioid," "Prescription opioids," "Synthetic opioids," "Heroin," "Stimulants," "Cocaine," "Psycho-stimulants," "Benzodiazepines," and "Antidepressants." Users can select one or multiple drug types to display in the visualizations.
- Year Range: A slider that lets users select a range of years for which they want to see data.
- Age Group: Radio buttons allow users to choose between "Young Adults, 15-24 Years" or "Overall" population data.
# Pending Features:
- Add a plot to display “Percentage of deaths related to synthetic opioid other than Methadone”.
- While our dashboard is rich in descriptive analytics, we plan to incorporate predictive models to forecast trends in overdose deaths.
# Difficulties and Challenges:
- Data preprocessing was out of expectation.
- Our dashboard does not just display data, it also includes metrics definition and calculations which is also a challenge.
# Deviations from Best Practices:
Our layout evenly weights all visualizations, which could dilute the focus on the most critical data points. Future designs will prioritize key metrics for a more guided user experience.
# Successes and Limitations:
- Success: The dashboard’s interactivity allows users to filter and customize the displayed information effectively.
- Limitation: The equal weighting of all visualizations may overwhelm users, and the absence of predictive analytics limits its scope as a forward-looking tool.
# Future Enhancements:
Integrating predictive analytics to project future trends.