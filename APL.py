from planning import search, searchParse
from completed import completed_search, compParse
from pFactor import runRel, idChecker, relFilter, filterList
from sheets import sheets


def APL():

    user = input("AniList username: ")
    
    sheetId = input("Google Sheets ID: ")

    search(user)
    searchParse()
    completed_search(user)
    compParse()
    filterList("planning")
    filterList("completed")
    runRel()
    relFilter()
    idChecker()
    sheets(sheetId)

APL()