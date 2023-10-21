from search import getRelationsData, planningSearch, completedSearch


def parseRelations(relation_data):
    parsed = relation_data["data"]["Media"]["relations"]["nodes"]

    parse_type = [x for x in parsed if x["type"] == "ANIME"]
    parse_format = [x for x in parse_type if x["format"] == "TV"]
    parse_status = [x for x in parse_format if x["status"] == "FINISHED"]

    return parse_status


def getIdFromRelations(relations_list):
    return [x["id"] for j in relations_list if j != [] for x in j]


def getRelations(completed_data):
    relations = []

    for x in range(len(completed_data)):
        relation_data = getRelationsData(completed_data[x])
        relations.append(parseRelations(relation_data))
        # print(round((x + 1) / len(completed_data) * 100, 1), "% Complete")

    return relations


def compareRelaltivePlan(relativeData, plan_id):
    for r in range(len(relativeData)):
        if relativeData[r] == plan_id:
            # print(relativeData[r], "is a match")
            return 0.1

    return 0


def bFactor(planning_data, bEps, bScore):
    for r in range(len(planning_data)):
        if 12 < bEps < 23:
            return max((bScore - 75) * pow(10, -2), 0)
        elif bEps >= 24:
            return max((bScore - 75) * pow(10, -2), 0) + (1 + max(0.05 * (bEps - 24), 0))/100
        else:
            return 0


def aplCalc(planning_data, aplScore, aplP, aplB, bWeight=0.5, pWeight=0.5):
    for r in range(len(planning_data)):
        return round(aplScore * (1 + (aplB * bWeight + aplP * pWeight)), 2)


def filterList(data):
    output = []

    for x in range(len(data)):
        output.append(data[x]["media"]["id"])

    return output


def getPFactorData(user):

    output = []

    planning_data = planningSearch(user)
    completed_data = completedSearch(user)
    completed_filtered = filterList(completed_data)
    relations_list = getRelations(completed_filtered)
    relation_ids = getIdFromRelations(relations_list)

    for i in range(len(planning_data)):
        planning_data[i]["media"]["pfactor"] = compareRelaltivePlan(
            relation_ids, planning_data[i]["media"]["id"]
        )
        planning_data[i]["media"]["bfactor"] = bFactor(
            planning_data, planning_data[i]["media"]["episodes"], planning_data[i]["media"]["averageScore"]
        )
        planning_data[i]["media"]["APL"] = aplCalc(
            planning_data, planning_data[i]["media"]["averageScore"], planning_data[
                i]["media"]["pfactor"], planning_data[i]["media"]["bfactor"]
        )

        output.append(planning_data[i]["media"])

    return output
