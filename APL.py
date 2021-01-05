from planning import search, searchParse
from completed import completed_search, compParse
from pFactor import runRel, idChecker, relFilter, filterList


def APL():

    user = input("AniList username: ")

    search(user)
    searchParse()
    completed_search(user)
    compParse()
    filterList("planning")
    filterList("completed")
    runRel()
    relFilter()
    idChecker()


APL()