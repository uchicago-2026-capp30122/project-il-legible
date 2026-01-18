# IL-legible

## Members

- Brock Sauvage <bsauvage@uchicago.edu>
- Elie Nowlis <enowlis@uchicago.edu>
- Max Manalang <manalang@uchicago.edu>
- Luke Friedman <lukef@uchicago.edu>

## Abstract

How does a bill become a law? In state governments across the country, including here in Illinois, that process is long and often hard to follow. In this project, we will examine what factors, if any, predict a bill’s eventual success - or lack thereof - in the **Illinois General Assembly**. Our goal is to uncover and communicate any clear patterns, information that we believe will be relevant to both political actors and engaged constituents.

One factor of particular interest is the bill’s sponsor and the sources of their previous campaign donations. Questions for exploration include:
- **Corporate Donations**: Do legislators who received large corporate donations introduce more bills than those who did not? Are there any patterns in the content of the bills they introduce? Any patterns in whether their bills eventually succeed or fail?
- **General Patterns**: In addition to a bill’s sponsors, is other data known at the time of a bill’s introduction predictive of its eventual outcome? These can include the committee the bill is referred to, the topic and contents of the bill, when in a legislative session it's introduced, etc.

## Preliminary Data Sources

### Data Source #1: Legiscan

- Source URL: <https://legiscan.com/legiscan>
- Source Type: API
- Summary: Provides JSON data on legislation in all 50 states. The data is very detailed, and Legiscan offers a [comprehensive user manual](https://api.legiscan.com/dl/LegiScan_API_User_Manual.pdf) for their datasets.
- Challenges: The free tier is limited to **30,000** queries per month. This likely won't be an issue, but it's worth keeping in mind as we dig into the data.

### Data Source #2: Plural / OpenStates

- Source URL: <https://open.pluralpolicy.com>
- Source Type: API + Bulk Download
- Summary: Another option for collecting data on state-level legislation, with good [API documentation](https://v3.openstates.org/docs#/jurisdictions/jurisdiction_list_jurisdictions_get).
- Challenges: Is this data easily aggregated at the State Legislature level?

### Data Source #3: Illinois Sunshine

- Source URL: <https://illinoissunshine.org/>
- Source Type: Web Scraping (CSVs)
- Summary: Provides detailed funding data for state and local candidates for office in Illinois. We can apply simple rules to see which donations came from entities (as opposed to individuals), but we would need to do our own industry classification of entities.
- Challenges: Donations are made to Candidate Committees, the naming conventions of which vary across candidates. We may need to do some manual Candidate <> Committee mapping.

### Data Source #4: Open Book - Illinois State Comptroller

- Source URL: <https://openbook.illinoiscomptroller.gov/>
- Source Type: Web Scraping
- Summary: Another option for data on donations, focused on both individuals and companies. Also provides data on state contract holders, which could be interesting data to cross-reference against active corporate donors.
- Challenges: Scraping this data in bulk might be challenging. We would need to start with a list of specific donors to search for, then scrape the results provided for each search. 

## Questions

1. Is there a large risk that we won’t find clear, *predictive* patterns for a bill’s success at the time it’s introduced? (If this happens, we'd likely shift focus to *descriptive* data analysis and visualization.)
2. Instead of predicting final enactment, would it make sense to focus on an intermediate outcome (e.g., whether a bill makes it out of committee) to narrow the problem?
3. Rather than analyzing both chambers of the Illinois General Assembly, would focusing on just one (House or Senate) be a useful way to simplify the project if needed?
4. Do you have an initial recommendation on how many years of legislative sessions to analyze? There's a likely tradeoff between a richer analysis with more data and the  complexity of additional data collection and cleaning.
5. Any recommendations on using Legiscan vs. Plural/OpenStates for data on legislation?