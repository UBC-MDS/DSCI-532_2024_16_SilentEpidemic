# Reflection for Milestone 4

## Brief reflection on insight, material, feedback
This week we spent our time mostly on polishing the look of the dashboard and fix any issues raised by our classmates/instructor.

That being said, we got to know a lot more how dash component works(https://dash.plotly.com/dash-core-components) and consulted a lot of online material e.g. w3school for css (https://www.w3schools.com/w3css/defaulT.asp).
## Current Implementation (With Changes Since Milestone 3)
1. Improve performance
  - Changed csvs to parquet to allow for data partitioning. 
  - Used memory cache for aggregated values for the aggregate values cards. This allows for saving outputs and faster subsequent processing times. Caching was not employed for the plots due to a higher memory requirement than for the single summary values. 
  - Removed row-wise operations from the opioid.py script and added the data processing to the preprocessing.py script.
2. Improve User Interface and User Experience:
  - Added tooltips and icons next to the plot title, especially if the plot title is not perfectly clear, or extra information is needed (e.g. some filters do not work for the demographic plot due to data limitation)
  - Added tooltips to clarify the charts’ behaviour and explaining the statistics shown.
  - Added a special chart for display error messages on top of the chart when the filter selection makes the charts unable to render data. 
  - Improved the layout of the sidebar, such as creating a reset button and making sure the drug type names don’t overlap. 
  - Aligned the colours of the drugs to avoid confusion resulting from the drug colour updating with changing filter selections, and also to ensure theme alignment across the dashboard.
  - Changed the demographic plot from a grouped bar chart to a line plot to improve readability across demographics. 
  - Added a favicon and plot title for site branding. 
  - Updated the “Percentage of Overdose Deaths Involving Opioids as a Secondary Factor” plot legend to remove duplication in drug type names. 
  - Fixed rounding to be consistent to one decimal place in the hover tooltips across all plots.  
  - Removed redundant words in the subtitles (ex/ selected drug types when the legend already lists this). 
  - Updated the subtitles to be consistent “Please select at least one drug type and one sex category” when there are no drug types or sexes selected in the plot. 
  - Added “x” to fold change card for readability. 
  - Fixed the accuracy of the aggregated value in death rate

## Known Issues
The legend of both main plot and the opioid plot are not in an ideal format. This is a known functionality gap in plotly - see [here](https://github.com/plotly/plotly.js/issues/5099).

## Deviations from Best Practices
The aforementioned legends.

## Difficulties and Challenges:
On the performance side we were not able to cache all plots, as this would be memory intensive for the many combinations of filter selections.
Using `joblib` to create file-based cache was considered, but since our callback functions does not contain heavy computations (i.e. every filter update only takes <500ms to update all charts), we suspect that using file-base caching would not bring much benefit in this case. We decided to cache the summary values only. No other significant difficulties were observed.

## Reflection on the Dashboard:
Our dashboard does a good job of visualizing the data and providing useful insights. We also believe our dashboard is self-explanatory and as well as a neat and easy to use layout.
Limitations are the same as for the previous reflections due to the nature of the dataset. Not every demographic feature can be further decomposed by gender, youth, etc. We would like the data to be even more granular since there are differences in overdose risk per community, and we hope our dashboard could be able to provide information specific to each school board.
A possible future addition related to the current dataset limitations would be to plot out drug overdose risk by state or community in a geospatial visualization to provide a granular interpretation of the overdose risk, and also to support with targeting teaching resources to where it is most needed. 
