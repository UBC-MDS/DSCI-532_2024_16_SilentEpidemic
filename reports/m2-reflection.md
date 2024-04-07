# Current Implementation
Our dashboard currently implements the following features from our proposal/sketch:
- Four Summary Information Cards: These provide a quick overview of key statistics including Overall Death, Death Rate, Percentage of young adults deaths, and Fold Change (2001-2015) (Overall/Young Adults).
- Main Bubble Chart: This shows the general trend of overdose deaths.
- Percentage of Deaths Related to Any Opioid: This provides specific insights into opioid-related deaths.
- Percentage of Deaths by Demographics: This allows for demographic-based (in particular the ethnicity) analysis.
- Filter Options: Users can filter the data by year, young adult (15-24 age group), drug type, and gender.

# Deviations from Proposal/Sketch
We decided to drop the plot for “Percentage of Deaths by Gender” because the same information can be shown in the main plot. This also prevents the dashboard from becoming crowded and the plots from becoming too small when three plots are displayed in one row.

# Known Issues
We are aware of the issue of double counting in the data. For example, adding the rate of each drug type will not yield the same total as the “Overall” category due to instances where multiple drugs are involved in a single death.

There is a divide by zero error in the OLS trendline added to the Percentage Opioid Deaths by Drug Type plot. This is to be addressed in a future milestone. 

# Deviations from Best Practices
We’ve adhered to DSCI531’s best practices, using distinct colors for categorical variables like ethnicity and limiting plot usage to avoid overwhelming users. Instead, we highlight key statistics with numeric cards. 

While it might be a better practice to use line charts for showing death rates of ethnicities over a period of time, we opted for a grouped bar chart since we aim to facilitate comparisons between groups instead of showing the overall trend (which our other plots have done).

# Difficulties and Challenges:
- Data preprocessing required considerable effort to generate useable plots and was out of the scope of the milestone. 
- Our dashboard does not just display data, it also includes metric definitions and calculations which took time to implement. 

# Reflections and Future Improvements:
Our dashboard does a good job of visualizing the data and providing useful insights. We also believe our dashboard is self-explanatory and as well as a neat  and easy to use layout.
However, it has some limitations due to the nature of the dataset. Not every demographic feature can be further decomposed by gender, youth, etc. Also, the issue of double counting presents a challenge for accurate representation of the data. Potential future improvements could include addressing these limitations and adding more interactive features to enhance user engagement.

Another possible enhancement would be to change the colour palette of the graphs, as the subject matter is very serious and the chart colours are not reflective of this (i.e. the colours appear to be too bright/cheerful for the topic). 

Additionally, we aim to explore fentanyl overdose trends due to its significant societal impact. As we deepen our data understanding, we hope to incorporate this in our next milestone.

