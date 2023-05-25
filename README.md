# Finds the name of a founder/CEO in the imprint (GER/ENG supported)
This small script retrieves the names of founders/CEO (Gründer/Geschäftsführer) from websites. 

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

Lists used:

#The imprint is usually separted in various parts. These words indicate that we reached a section which wont contain our desired names
ListOfWordsToClean = ["Kontakt", "Umsatzsteuer", "Hausanschrift", "E-Mail"]

#List of possible subsites with the name of the CEO/Founder
 ListOfImprintWords = ["impressum", "imprint", "policies/legal-notice","impressum.html", "legal-disclaimer", "legals"]

#List of possible CEO/Founder synonyms
ListOfCEOKeywords = ["Geschäftsführe", "Managing Directors:", "Vertreten durch", "Representative","Vertreten durch die Geschäftsführer","Verantwortliche", "CEO", "Vertretungsberechtigt", "legal representative", "Gesellschafter", "Vertreten durch Geschäftsführer", "Verantwortlich für", "Represented by", "Members of the Board", "Geschäftsführung", "Geschäftsführende Gesellschafter"]  
