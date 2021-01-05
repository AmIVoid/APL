import json
import requests
from ratelimit import limits, sleep_and_retry
import os

RATE_LIMIT = 60
CALLS = 85


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def getRelationsData(listId):
    url = "https://graphql.anilist.co"
    query = """
	query($id: Int) {
    Media(id: $id, type: ANIME) {
        id
        title {
            romaji
        }
        relations {
            nodes {
                id
                type
                format
                status
                title {
                    romaji
                }
            }
        }
    }
}
	"""

    variables = {"id": listId}

    response = requests.post(url, json={"query": query, "variables": variables})

    if response.status_code != 200:
        raise Exception("API response: {}".format(response.status_code))

    return json.loads(response.text)


def parseRelations(relation_data):
    # print(relation_data["data"])
    parsed = relation_data["data"]["Media"]["relations"]["nodes"]

    parse_type = [x for x in parsed if x["type"] == "ANIME"]
    parse_format = [x for x in parse_type if x["format"] == "TV"]
    parse_status = [x for x in parse_format if x["status"] == "FINISHED"]

    return parse_status


def relFilter(relations_list):
    return [x["id"] for j in relations_list if j != [] for x in j]


def runRel(completed_data):
    relations = []

    for x in range(len(completed_data)):
        relation_data = getRelationsData(completed_data[x])
        relations.append(parseRelations(relation_data))
        print(round((x + 1) / len(completed_data) * 100, 1), "% Complete")

    return relations


def idChecker(planning_data, relations_id):
    output = []

    for i in range(len(planning_data)):
        planning_data[i]["media"]["pfactor"] = compareRelaltivePlan(
            relations_id, planning_data[i]["media"]["id"]
        )
        output.append(planning_data[i]["media"])

    planOutput = json.dumps(output, indent=4)
    print(planOutput, file=open("p_planning.json", "w"))


def compareRelaltivePlan(relativeData, plan_id):
    for r in range(len(relativeData)):
        if relativeData[r] == plan_id:
            print(relativeData[r], "is a match")
            return 0.1

    return 0


def filterList(data):
    output = []

    for x in range(len(data)):
        output.append(data[x]["media"]["id"])

    return output