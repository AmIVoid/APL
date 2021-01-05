from planning import search, searchParse
from completed import completed_search, compParse
from pFactor import runRel, idChecker, relFilter, filterList


def APL():

    user = input("AniList username: ")

    planning_data = search(user)
    completed_data = completed_search(user)
    completed_filtered = filterList(completed_data)
    relations_list = runRel(completed_filtered)
    relation_ids = relFilter(relations_list)
    idChecker(planning_data, relation_ids)


APL()