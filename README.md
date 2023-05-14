# FounderImprintCrawler
This small script retrieves the names of founders/CEO from websites. 

Process:
- Tries finding the imprint page with the help of a list with imprint synonyms
- This list will be exported to an excel
- Excel will be read again
- Search in the imprint for the specified keywords in the list "ListOfCEOKeywords"
- If found, the script knows 6-7 cases and will take the names
- list of names is exported again

Required dependencies:
- re, requests, html, pands

Required additional files:
- Excel list with websites to search in

!Must read!
The lists contain synonyms, which are frequently used by german startups for CEO/Founder. Thus its a mix of german and english words.
