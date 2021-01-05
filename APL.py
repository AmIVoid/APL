from search import planningSearch, completedSearch
from pFactor import runRel, idChecker, relFilter, filterList
from sheets import sheets


def APL():

    user = input("AniList username: ")

    sheetId = input("Google Sheets ID: ")

    planning_data = planningSearch(user)
    completed_data = completedSearch(user)
    completed_filtered = filterList(completed_data)
    relations_list = runRel(completed_filtered)
    relation_ids = relFilter(relations_list)
    idChecker(planning_data, relation_ids)
    sheets(sheetId)


APL()