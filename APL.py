from planning import search, searchParse
from completed import completed_search, compParse
from pFactor import runRel, idChecker, relFilter, filterList
from sheets import sheets


def APL():

    user = input("AniList username: ")
    
    sheetId = input("Google Sheets ID: ")

    planning_data = search(user)
    completed_data = completed_search(user)
    completed_filtered = filterList(completed_data)
    relations_list = runRel(completed_filtered)
    relation_ids = relFilter(relations_list)
    idChecker(planning_data, relation_ids)
    sheets(sheetId)

APL()