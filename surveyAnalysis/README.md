Survey_analysis.ipynb notebook has the code used for preprocessing, exploration, and analysis of the data collected through the survey we compiled along with other participants of the data challenge under the guidance of TCS A&I team. 


Broad Overview of steps - 

1. Pre-processing: The data, although structured for the most part had a few unwanted data. So, a little of pre-processing had to be done to get the data in proper dataframe format. 

2. Clustering: K Means clustering technique was used to cluster the repondents and further analysis was done using 2 clusters as the silhoutte score for k-2 was better compared to the other k values. Features used for clustering included basic information about respondents like country, education, and their interpretation of the pandemic. 

3. Exploration and Analysis: Once the clusters were decided, we moved on to analyzing the rest of the data to understand if there was any significant difference between the clusters in the other responses which were and were not used for clustering. Althought the clusters were not significantly different, there were a few observations that were very interesting to capture. 

NOTE: The reason why we decided to so is because google forms itself has this superb ability to provide detailed statistics and visualizations. We wanted to explore the data in a different and interesting way. 
