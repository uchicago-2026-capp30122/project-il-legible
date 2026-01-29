# IL-legible
Team Members: Max, Luke Friedman, Eliana Nowlis

## Abstract

How does a bill become a law? In state governments across the country, including here in Illinois, that process is long and often hard to follow. In this project, we will examine what factors, if any, predict a bill’s eventual success - or lack thereof - in the **Illinois General Assembly**. Our goal is to uncover and communicate any clear patterns, information that we believe will be relevant to both political actors and engaged constituents.

We are particularly interested in the following factors:
- **Sponsorships**: Does who supports the bill make it more likely to pass? Do legislators who received large corporate donations introduce more bills than those who did not? Do the sources of sponsers' campaign donations or the total amount raised make a difference?
- **Timing**: Do bills introduced towards the end of a legislate session tend to get passed more? Does the length of time between the introduction and further actions matter? Are bills that break timing rules more likely to pass?
- **Voting and Chambers**: Does the amount or distribution of votes in one chamber impact the outcome in the other? Does which chamber the bill was introduced in matter?

## Data Sources

### Data Source #1 [BROCK/LUKE TO DO]

Source URL: {https://...}  
Source Type: {Scraped/Bulk Data/API}  
Approximate Number of Records (rows):  
Approximate Number of Attributes (columns):   
Current Status: {At this point, you should have interacted with your data, describe the current status. Have you written code for an API or web scraper yet, explored the data, etc.?}  
Challenges: {Any challenges or uncertainty about the data at this point?}

### Data Source #2

Source URL: https://illinoissunshine.org/  
Source Type: Scraped/API -- will need to access hidden APIs to download CSVs of each committee individually  
Approximate Number of Records (rows): ~ 100 donations x 300 politicians  
Approximate Number of Attributes (columns): 31  
Current Status: The data have been explored and specific committees have been scraped. The next step is to isolate the committees we need from the Open States data and write a code to download information from each related API.  
Challenges: We are still unsure how we will identify donations from corporations versus individuas.  

## Data Reconciliation Plan

We will connect the **Open States** data to the **Illinois Sunshine** data using the name of the politician/sponser and the committee they belong to. In the Open States data this information can be found under the Sponserships list of dictionaries, which includes the names of politicians sponsering the bill. Once we have a complete list of politicians we are interested in, we can link these to their corresponding committee present in the Illinois Sunshine data. This link may be done programmatically, but manual work would also be doable due to the fact that there are less than 200 politicians each session.

## Project Plan

Step 1: Preliminary setup and exploration (by Feb 4th)
1) Set up GitHub repository with a nice layout (plan to have code executable from the command line) [Elie/Brock]
2) Data exploration to ID key variables [All]

Step 2: Collect data (by Feb 11th)
4) Collect the Open States data [Luke/Brock]
4) Get a list of the politicians we care about [Luke/Brock] and link them to their committees [Elie/Max]
5) Get Illinois Sunshine data for those committees [Elie/Max]

**Note**: We will divide up work in further weeks depending on availability.

Step 3: Data analysis (by Feb 18th)
6) Figure out what information we want from the Illinois Sunshine data
5) Clean and merge the datasets
6) Run predictive analyses using complete data (and key variables)
5) If we find nothing interesting,  find new things to look at
3) Explore possible data visualizations (come up with ideas using mock data)

!! Week 7 prototype due Feb 22nd !!

Step 4: Create output (by March 4)
2) Make a database framework [Brock]
7) Create visualization using complete data
8) Figure out presentation + make pretty
9) Turn into a website (?) [Brock]

Step 5: Finalizing project (by March 8)
8) Create tests (6-9 total)
9) Create a README, internal documentation, and demo video

!! Full project due March 9th !!

## Questions

1. N/A (answered in office hours)