# IL-legible
Team Members: Max, Luke Friedman, Eliana Nowlis, Brock Sauvage

## Abstract

How does a bill become a law? In state governments across the country, including here in Illinois, that process is long and often hard to follow. In this project, we will examine what factors, if any, predict a bill’s eventual success - or lack thereof - in the **Illinois General Assembly**. Our goal is to uncover and communicate any clear patterns, information that we believe will be relevant to both political actors and engaged constituents.

We are particularly interested in the following factors:
- **Sponsorships**: Does who supports the bill make it more likely to pass? Do legislators who received large corporate donations introduce more bills than those who did not? Do the sources of sponsers' campaign donations or the total amount raised make a difference?
- **Timing**: Do bills introduced towards the end of a legislate session tend to get passed more? Does the length of time between the introduction and further actions matter? Are bills that break timing rules more likely to pass?
- **Voting and Chambers**: Does the amount or distribution of votes in one chamber impact the outcome in the other? Does which chamber the bill was introduced in matter?

## Data Sources

| Data Source | Source URL | Type | Approx. Number of Records | Approx. Number of Attributes | Current Status | Challenges |
| --- | --- | --- | --- | --- | --- | --- |
| Open States | https://docs.openstates.org/api-v3/  | API/Bulk Data | Approx. Number of Records | Approx. Number of Attributes | Data Exploration via API and Bulk Data Download | Internal IDs might not reconcile well with other data sources |
| Illinois Sunshine | https://illinoissunshine.org/ | Scraped/API -- will need to access hidden APIs to download CSVs of each committee individually  | ~ 100 donations x 300 politicians   | 31  | The data have been explored and specific committees have been scraped. The next step is to isolate the committees we need from the Open States data and write a code to download information from each related API.  | We are still unsure how we will identify donations from corporations versus individuas.  |

## Data Reconciliation Plan

We will connect the **Open States** data to the **Illinois Sunshine** data using the name of the politician/sponser and the committee they belong to. In the Open States data this information can be found under the Sponserships list of dictionaries, which includes the names of politicians sponsering the bill. Once we have a complete list of politicians we are interested in, we can link these to their corresponding committee present in the Illinois Sunshine data. This link may be done programmatically, but manual work would also be doable due to the fact that there are less than 200 politicians each session.

## Project Plan

*Step 1*: Preliminary setup and exploration (by Feb 4th)
1) Set up GitHub repository with a nice layout (plan to have code executable from the command line) [Elie/Brock]
2) Data exploration to ID key variables [All]

*Step 2*: Collect data (by Feb 11th)

3) Collect the Open States data [Luke/Brock]
4) Get a list of the politicians we care about [Luke/Brock] and link them to their committees [Elie/Max]
5) Get Illinois Sunshine data for those committees [Elie/Max]

**Note**: We will divide up work in further weeks depending on availability.

*Step 3*: Data analysis (by Feb 18th)

6) Figure out what information we want from the Illinois Sunshine data
7) Clean and merge the datasets
8) Run predictive analyses using complete data (and key variables)
9) If we find nothing interesting,  find new things to look at
10) Explore possible data visualizations (come up with ideas using mock data)

**!! Week 7 prototype due Feb 22nd !!**

*Step 4*: Create output (by March 4)

11) Make a database framework [Brock]
12) Create visualization using complete data
13) Figure out presentation + make pretty
14) Turn into a website (?) [Brock]

*Step 5*: Finalizing project (by March 8)

15) Create tests (6-9 total)
16) Create a README, internal documentation, and demo video

**!! Full project due March 9th !!**

## Questions

1. N/A (answered in office hours)