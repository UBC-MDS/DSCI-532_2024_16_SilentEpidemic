# Reflection for Milestone 3

## Current Implementation (With Changes Since Milestone 2)
Our dashboard currently implements the following updates to the dashboard features, as requested by the instructor and agreed upon as a team:

Four Summary Information Cards: 
- Shifted up the card panes to be aligned with the top of the filter pane for visual appeal. The values of the cards are also made to keep aligned vertically with each other to keep visual uniformity.

Percentage of Deaths Related to Any Opioid Plot: 
- This plot was updated to reflect feedback that the plot is ambiguous and is not easily understandable. This was addressed by updating the plot title for clarity (“Percentage of Deaths Related to Any Opioid” was changed to “Percentage of Overdose Deaths Involving Opioids as a Secondary Factor”). The plot was also updated from a scatter plot with an ordinary least squares trendline, to a dual-line plot, with one line per gender. This allows users to see the trend in overdoses resulting from polysubstance abuse (a certain drug type in addition to opioids) over time. Lastly, the points and trendlines at 100% were removed for the opioid drug classes, as this was confusing for users. Instead, if the user selects opioid drug classes (`Prescription opioids`, `Synthetic opioids`, or `Heroin`) in the global filter pane, the plot will show all other drug types excluding the opioid drug classes as the default. If the user selects any of the non-opioid drug classes, the plot will show the percentage of overdose deaths involving opioids for each of those drug types. 

Percentage of Deaths by Demographics Plot: 
- In Milestone 2, there was an issue of double counting of total rate because of the hierarchy of the data (i.e. some drug types belong to opioids). We have removed the option of `Any opioid` to make the selections easily understandable, and solves this issue.

Filter Options: 
- In Milestone 3, we have used css to format each selection, ensuring they are visible and clear. We also added horizontal lines between them and rearranged the filters in a logical manner.

Code Modularization: 
- Code was modularized into scripts, modules and assets, in order to improve readability for end users (rather than having one long app.py file) and improve accessibility for future updates or changes.

Colour palette: 
- In Milestone 2, it was identified that the colour palette of the plot was quite “cheerful” as compared to the serious nature of the topic. This has been addressed by changing the main chart’s color palette to `px.colors.qualitative.Prism` and the one for opioid and demographic chart to `px.colors.qualitative.T10`. The reason for choosing two different color palettes for our charts is that `Prism` is too sharp on the lines and bars, while `T10` appears visually unappealing when applied on large bubbles. These two palettes are comparable in the colours they used, and the uniformity of our dashboard in terms of colour choices is still preserved.

## Known Issues
The loading time of the Render web app is very slow, and takes up to 5 minutes to load the dashboard. This is not acceptable for production and will require additional troubleshooting in Milestone 4.

## Deviations from Best Practices
While it might be a better practice to use line charts for showing overdose death rates related to a specific ethnicity over a period of time, we opted for a grouped bar chart since we aim to facilitate comparisons between groups instead of showing the overall trend (which our other plots have done).
Additionally, in the feedback given by the instructor it has been suggested that a legend is to be added at the main bubble chart to denote the actual number represented for different sizes of the markers. It has been found out that `plotly`, the library we have been using for creating the chart, does not support this type of legend yet (refer to plotly/plotly.py#3505 plotly/plotly.js#5099). Workaround exists but this will significantly affect the layout of the dashboard. Therefore, the plan to add the said legend is scrapped. Instead, the chart’s subtitle has been changed to inform the size of the marker is proportional to the death rate, and encourages users to check the actual death rates by hovering their cursors using the chart’s interactive tooltips.

## Difficulties and Challenges:
No significant difficulties were observed, as compared to Milestone 2, which required significant upfront work for data preprocessing.

## Reflections and Future Improvements:
Our dashboard does a good job of visualizing the data and providing useful insights. We also believe our dashboard is self-explanatory and as well as a neat and easy to use layout. However, it has some limitations due to the nature of the dataset. Not every demographic feature can be further decomposed by gender, youth, etc. A more thorough dataset would allow for additional plots within the dashboard and increased data exploration. 