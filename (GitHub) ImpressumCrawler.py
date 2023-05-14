# -*- coding: utf-8 -*-
"""
@author: FabPei
@version: 13052023

"""

import re
import requests
import html
import pandas as pd

#This method tries to clean a given string of any html leftovers
def cleanString(string):
    if not string.find("\n") == -1:
        string = string.replace("\n", "")
    for Keyword in ListOfWordsToClean:
        IntPosKeyword = string.find(Keyword)
        if not IntPosKeyword -1:
            string = string[:IntPosKeyword]
    IntPosKeyword = -1
    IntPosKeyword = string.find("<")       
    if not IntPosKeyword-1:
        string = string[:IntPosKeyword]
    if string[0:0] == ">":
        string = string[1:]
    
    return string

#Method for importing a certain column into a list
def ExcelColumnToList(ExcelPath, ColumnName):
    data = pd.read_excel (ExcelPath) #place "r" before the path string to address special character, such as '\'. Don't forget to put the file name at the end of the path + '.xlsx'
    df = pd.DataFrame(data, columns = [ColumnName])
    ListOfWebsites = df[ColumnName].tolist()
    return ListOfWebsites

#Test if imprint exists, uses the keyword list for imprint synonyms
def TestImprint(List, KeywordList):
    ListWebsitesTested = []
    i = 0
    for WebsiteLink in List:
        print(WebsiteLink)
        if WebsiteLink == "" or WebsiteLink == " " or WebsiteLink == None or len(WebsiteLink) < 3:
            continue
        ListWebsitesTested.insert(i, WebsiteLink)
        for Keyword in KeywordList:    
            ElementInserted = False
            
            if WebsiteLink[10:].find(r"/") == -1:
                
                WebsiteLinkImp = WebsiteLink + r"/" + Keyword
            else:
                WebsiteLinkImp = WebsiteLink[:WebsiteLink[:].rfind(r"/") + 1] + Keyword
            
            try:
                r = requests.get(WebsiteLinkImp)
                if r.text.find("error-404") > -1 or r.text.find("404 Not Found") > -1:
                    continue
            except:
                continue
                
            
            if r.status_code == 404:
                ListWebsitesTested[i] = "Error Code 404 " + WebsiteLink 
                ElementInserted = True
                continue
            else:
                ListWebsitesTested[i] = WebsiteLinkImp
                ElementInserted = True
                break
        if ElementInserted == False: #WEBSITE IS PROBABLY DEAD
            ListWebsitesTested[i] = "Unknown error " + WebsiteLink
            pass
        i += 1
        
    return ListWebsitesTested

def FindCutArea(html):
    pattern = "\d\d\d\d\d\s([\u00C0-\u017FA-Z])([\u00C0-\u017Fa-z])([\u00C0-\u017Fa-z]).+"
    compiled = re.compile(pattern)
    ms = compiled.search(html)
    return html

#This method searches the imprint for the keywords specified in "ListOfCEOKeywords"
def SearchImprint(List, KeywordList):
    
    ListOfCEOS = []
    i = 0
    
    for WebsiteLink in List:
        ListOfCEOS.insert(i, WebsiteLink)
        try:
            r = requests.get(WebsiteLink)  
            r.encoding = "UTF-8"
            result = html.unescape(r.text)
            result = FindCutArea(result)
        except:
            result = "Error"
            ListOfCEOS[i] = "Error"
            i = i + 1
            continue
        
        for Keyword in KeywordList:            
            IntIndexKeyword = result.lower().find(Keyword.lower())
            if IntIndexKeyword == -1:
                print("not found " + Keyword + " in " + WebsiteLink + "\n")
                pass
            else:
                print("found " + Keyword + " in " + WebsiteLink)
                
                ListOfCEOS[i] = cleanString(GetChiefName(IntIndexKeyword, result, Keyword))
                break
            
        try:  
            if ListOfCEOS[i] is None:
                pass
        except:
            if result.find("403 Forbidden"):
                ListOfCEOS[i] = "Bad website error, site was created but is private"
            else:
                ListOfCEOS[i] = "Nothing Found"
            pass
        
        i = i + 1
    return ListOfCEOS 


#This method will try to find names in the html maze
def GetChiefName(Index, html, Keyword):

    html = html[:Index + 500]
    ###check for continuation -> names are attached to another: NameName
    pattern = "([\u00C0-\u017Fa-z]):\s([\u00C0-\u017FA-Z])+"
    compiled = re.compile(pattern)
    IntEndOfCEOWord = html[Index:].find(":")
    ms = compiled.search(html[Index + IntEndOfCEOWord - 3:Index + IntEndOfCEOWord + 5])
    try:

        print("CASE: CONTINUUM")
        IntEndOfKeyword = html[Index + ms.start():].find(r"<")

        return html[Index + ms.start() + IntEndOfCEOWord: Index + ms.start() + IntEndOfKeyword]  
    except:
        pass
    ##
    
    ###check for coninuation2 doublespace -> if there is an doublespace
    pattern = "([\u00C0-\u017Fa-z]):\s\s([\u00C0-\u017FA-Z])"
    compiled = re.compile(pattern)
    IntEndOfCEOWord = html[Index:].find(":")
    ms = compiled.search(html[Index + IntEndOfCEOWord - 3:Index + IntEndOfCEOWord + 5])

    try:

        print("CASE: CONTINUUM2")
        IntEndOfKeyword = html[Index + IntEndOfCEOWord + 3:].find(r"  ")

        return html[Index + IntEndOfCEOWord + 3:Index + IntEndOfKeyword + IntEndOfCEOWord + 3]  
    except:
        print("NOT CONT2")
        pass
    ##
    
     ###check for coninuation 3 ->happens
    pattern = r"\s([\u00C0-\u017FA-Z])([\u00C0-\u017Fa-z])([\u00C0-\u017Fa-z])"
    compiled = re.compile(pattern)
    ms = compiled.search(html[Index + len(Keyword):Index + len(Keyword) + 5])
    try:

        print("CASE: CONTINUUM3")
        IntEndOfKeyword = html[Index + len(Keyword):].find(r"<")

        return html[Index + len(Keyword) + 1:Index + len(Keyword) + IntEndOfKeyword]
    except:
        pass
    ##   
    
    ###check for coninuation 4
    pattern = r"([\u00C0-\u017Fa-z])([\u00C0-\u017Fa-z]):<"
    compiled = re.compile(pattern)
    IntEndOfCEOWord = html[Index:].find(":")
    ms = compiled.search(html[Index + IntEndOfCEOWord - 5:Index + IntEndOfCEOWord + 5])
    
    try:
        IntEndOfKeyword = html[Index + IntEndOfCEOWord + 4:].find(r">")
        IntEndOfKeyword = IntEndOfKeyword + html[Index + IntEndOfCEOWord + 4 + IntEndOfKeyword:].find(r">")
        IntEndOfKeyword = IntEndOfKeyword + html[Index + IntEndOfCEOWord + 4 + IntEndOfKeyword:].find(r"<")

        return html[Index + IntEndOfCEOWord + 4 + IntEndOfKeyword:IntEndOfKeyword]  
    except:
        pass
    ##

    ###Check for backwards: for some reason, the names can be mixed up
    pattern = "\s–\s"
    compiled = re.compile(pattern)
    ms = compiled.search(html[Index - 5:Index])
    try:

        print("CASE: Backwards") 
        IntEndOfKeyword = html[:Index].rfind(r">")

        return html[IntEndOfKeyword:Index - 3]
    except:
        pass   
    ##
    
    ###check name handling -> weird case
    pattern = r"[>]\s([\u00C0-\u017FA-Z]).+[\s].+([\u00C0-\u017FA-Z\S]).+[<]"
    compiled = re.compile(pattern)
    ms = compiled.search(html[Index:])
    try:

        print("CASE: NAME") 
        IntEndOfKeyword = html[Index + ms.start(): ].find(r"<")

        return html[Index + ms.start():Index + ms.start() + IntEndOfKeyword]
    except:
        pass   
    ##

    IntEndOfKeyword = html[Index: ].find("\n")

    if IntEndOfKeyword > 50:
        intDoubleP = html[Index: ].find(r":") 
        if html[Index + intDoubleP: ].find(r"<br>") < 15 and html[Index: ].find(r"<br>") > -1:

            IntEndOfKeyword = html[Index: ].find(r"<br>")
            IntEndOfChief = html[Index + IntEndOfKeyword + 1:].find(r"<br>")
            ChiefName = html[Index + IntEndOfKeyword : Index + IntEndOfChief + IntEndOfKeyword]        
            ChiefName = cleanString(ChiefName)

            return ChiefName
        elif html[Index + intDoubleP: ].find(r"<p>") < 8:

            IntEndOfKeyword = html[Index: ].find(r"</p>")
            IntEndOfChief = html[Index + IntEndOfKeyword + 1:].find(r"</p>")
            IntBegOfChief = html[: Index + IntEndOfKeyword + IntEndOfChief].rfind(r"<p>")

            ChiefName = html[IntBegOfChief : IntBegOfChief + IntEndOfChief]        
            ChiefName = cleanString(ChiefName)
 
            return ChiefName           
    elif IntEndOfKeyword < 50 and IntEndOfKeyword >= 0:

        IntEndOfChief = html[Index + IntEndOfKeyword + 1:].find("\n")

        ChiefName = html[Index + IntEndOfKeyword : Index + IntEndOfChief + IntEndOfKeyword]
        ChiefName = cleanString(ChiefName)
 
        return ChiefName
    elif IntEndOfKeyword == -1:

        IntEndOfKeyword = html[Index: ].find(r"<br/>")
        if IntEndOfKeyword == -1:
            pattern = ">([\u00C0-\u017FA-Z])"
            compiled = re.compile(pattern)
            try:
                ms = compiled.search(html[Index:])

                IntEndOfKeyword = html[Index + ms.start():].find(r"<")

                return html[Index + ms.start() + 1: Index + IntEndOfKeyword + ms.start()]
            except:
                pass
            
            pass
        else:
            IntEndOfChief = html[Index + IntEndOfKeyword + 1:].find(r"<br/>")
            ChiefName = html[Index + IntEndOfKeyword + 5 : Index + IntEndOfChief + IntEndOfKeyword]        
            ChiefName = cleanString(ChiefName)
      
            AfterFirstChief = html[Index + IntEndOfChief + IntEndOfKeyword + 2 : ].find(r"<br/>")
            if AfterFirstChief > -1:
                IntSecondChiefNameBeg = html[ : AfterFirstChief + Index + IntEndOfChief + IntEndOfKeyword + 2].rfind(r"<br/>")
                SecondChiefName = html[IntSecondChiefNameBeg + 5: AfterFirstChief + Index + IntEndOfChief + IntEndOfKeyword + 2]                
                return ChiefName + ", " + SecondChiefName
        
    return "Nothing found"      

#The imprint is usually separted in various parts. These words indicate that we reached a section which wont contain our desired names
ListOfWordsToClean = ["Kontakt", "Umsatzsteuer", "Hausanschrift", "E-Mail"]
 #List of possible subsites with the name of the CEO/Founder
ListOfImprintWords = ["impressum", "imprint", "policies/legal-notice","impressum.html", "legal-disclaimer", "legals"]
#List of possible CEO/Founder synonyms
ListOfCEOKeywords = ["Geschäftsführe", "Managing Directors:", "Vertreten durch", "Representative","Vertreten durch die Geschäftsführer","Verantwortliche", "CEO", "Vertretungsberechtigt", "legal representative", "Gesellschafter", "Vertreten durch Geschäftsführer", "Verantwortlich für", "Represented by", "Members of the Board", "Geschäftsführung", "Geschäftsführende Gesellschafter"]           

#Part 1: Get a list (excel) with imprint URLs
ListOfWebsites = ExcelColumnToList("Input2.xlsx", 'Link') #Excel table with lots of websites in column A, A1 should be named "Link"

ListWebsitesImprint = TestImprint(ListOfWebsites, ListOfImprintWords)
df = pd.DataFrame(ListWebsitesImprint)
df.columns=["Link"]
writer = pd.ExcelWriter("Output.xlsx",  engine="xlsxwriter")
df.to_excel(writer, index=False)
writer.save()
writer.close()
##

#Part 2: Go through every imprint and try to retrieve the name(s) of the CEO/Founder
ListWebsitesImprint = ExcelColumnToList("Output.xlsx", "Link") 
SearchedList = SearchImprint(ListWebsitesImprint, ListOfCEOKeywords)
dictionary = {"Link":ListWebsitesImprint, "Chief":SearchedList}
df = pd.DataFrame(dictionary)
writer = pd.ExcelWriter("Chief.xlsx",  engine="xlsxwriter") #Final output
df.to_excel(writer, index=False)
writer.save()
writer.close()
##

    
