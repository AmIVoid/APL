from planning import search, searchParse
from completed import completed_search, compParse
from pFactor import runRel, idChecker, planFilter, compFilter, relFilter

def APL():
    
    user = input("AniList username: ")
    
    search(user)
    searchParse()
    completed_search(user)
    compParse()
    planFilter()
    compFilter()
    runRel()
    relFilter()
    idChecker()
    
APL()