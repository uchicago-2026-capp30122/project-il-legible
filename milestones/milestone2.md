# {IL-legible}
Team Members: Max, 

## Abstract

How does a bill become a law? In state governments across the country, including here in Illinois, that process is long and often hard to follow. In this project, we will examine what factors, if any, predict a bill’s eventual success - or lack thereof - in the **Illinois General Assembly**. Our goal is to uncover and communicate any clear patterns, information that we believe will be relevant to both political actors and engaged constituents.

One factor of particular interest is the bill’s sponsor and the sources of their previous campaign donations. Questions for exploration include:
[[DO WE WANT TO UPDATE THESE TO THE THINGS WE TALKED TO JAMES ABOUT]]
- **Corporate Donations**: Do legislators who received large corporate donations introduce more bills than those who did not? Are there any patterns in the content of the bills they introduce? Any patterns in whether their bills eventually succeed or fail?
- **General Patterns**: In addition to a bill’s sponsors, is other data known at the time of a bill’s introduction predictive of its eventual outcome? These can include the committee the bill is referred to, the topic and contents of the bill, when in a legislative session it's introduced, etc.

-> Specifically looking at Classificaiton = Bill
-> Last Passage Date to see if it passed

## Data Sources

### Data Source #1 [BROCK/LUKE TO DO]

Source URL: {https://...}
Source Type: {Scraped/Bulk Data/API}
Approximate Number of Records (rows):
Approximate Number of Attributes (columns): 
Current Status: {At this point, you should have interacted with your data, describe the current status. Have you written code for an API or web scraper yet, explored the data, etc.?}
Challenges: {Any challenges or uncertainty about the data at this point?}

### Data Source #2 [ELIE TO DO]

Source URL: https://illinoissunshine.org/
Source Type: Scraped/Bulk Data -- will need to scrape website to download CSVs of each [[committtee]] individually
Approximate Number of Records (rows):
Approximate Number of Attributes (columns): 
Current Status: {At this point, you should have interacted with your data, describe the current status. Have you written code for an API or web scraper yet, explored the data, etc.?}
Challenges: We are still unsure how we will identify donations from corporations versus individuas

## Data Reconciliation Plan

We will connect the Open States data to the Illinois Sunshine data using the name of the politician/sponser. In the Illinois Sunshine data this information comes from [[what did Luke pull?]]. In the Open States data this informaiton can be found under the Sponserships list of dictionaries, which includes the names of politicians sponsering the bill. Because these data are names and will not match perfectly, we plan to use [[something]] to create a lookup that links these two datasets. We plan to do some amount of manual work, which should be doable due to the fact that there are [[less than 200]] politicians each session.

## Project Plan

Step 1: Preliminary setup and exploration (by Feb 4th)
1) Set up GitHub repository with a nice layout (plan to have code executable from the command line)
2) Data exploration to ID key variables: currently interested in exploring sponsorships (linked to donations), timing between bill introductions and readings, distribution of votes, outliers/rule breaks in actions, timing of bill introduction, where it started

Step 2: Collect data (by Feb 11th)
4) Collect the Open States data [Luke/Brock]
4) Get a list of the politicians we care about [Luke/Brock] and link them to their committees [Elie/Max]
5) Get Illinois Sunshine data for those committees [Elie/Max]

Step 3: Data analysis (by Feb 18th)
6) Figure out what we want from Sunshine data and add it to the other one
5) Clean and merge the data
6) Do deeper variable analysis using complete data (ID key variables)
    7) Run a predictive analysis
5) If failure find new things to look at
3) Explore possible data visualizations (come up with ideas using mock data)
!! Week 7 prototype due Feb 22nd !!

Step 4: Create output (by March 4)
2) Make a database framework (??) [Brock]
7) Create visualization using complete data
8) Figure out presentation + make pretty
9) Website [Brock]

Step 5: Finalizing project (by March 8)
8) Create tests (6-9 total)
9) Create a README, internal documentation, demo video
!! Full project due March 9th !!

## Questions

1. {A *numbered** list of questions for us to respond to.}
2. {...}