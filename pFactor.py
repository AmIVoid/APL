import json
import requests
from ratelimit import limits, sleep_and_retry
import os

RATE_LIMIT = 60
CALLS = 85


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def relations(listId):
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

    url = "https://graphql.anilist.co"

    response = requests.post(url, json={"query": query, "variables": variables})

    text_out = response.text

    with open("rel.json", "w") as out_file:
        out_file.write(text_out)


def parseRel():
    with open("rel.json") as json_data:
        data = json.load(json_data)

    parsed = data["data"]["Media"]["relations"]["nodes"]

    parse_type = [x for x in parsed if x["type"] == "ANIME"]

    parse_format = [x for x in parse_type if x["format"] == "TV"]

    parse_status = [x for x in parse_format if x["status"] == "FINISHED"]

    objects = json.dumps(parse_status, indent=4)

    with open("relations.json", "w") as out_file:
        out_file.write(objects)

    os.remove("rel.json")


def planFilter():
    with open("planning.json") as jsonData:
        planData = json.load(jsonData)

    output = []

    f = 0

    for x in range(len(planData)):
        output.append(planData[f]["media"]["id"])
        f += 1

    planObjects = json.dumps(output, indent=4)

    with open("planning_filtered.json", "w") as out_file:
        out_file.write(planObjects)


def compFilter():
    with open("completed.json") as jsonData:
        compData = json.load(jsonData)

    output = []

    f = 0

    for x in range(len(compData)):
        output.append(compData[f]["media"]["id"])
        f += 1

    compObjects = json.dumps(output, indent=4)

    with open("completed_filtered.json", "w") as out_file:
        out_file.write(compObjects)


def relFilter():
    with open("all_rel.json") as jsonData:
        relData = json.load(jsonData)

    output = []

    aList = 0
    i = 0

    for x in range(len(relData)):
        if relData[aList] == "[]":
            aList += 1
        else:
            for x in range(len(relData[aList])):
                output.append(relData[aList][i]["id"])
                i += 1

        aList += 1
        i = 0

    relObjects = json.dumps(output, indent=4)

    with open("relations_filtered.json", "w") as out_file:
        out_file.write(relObjects)


def runRel():
    with open("completed_filtered.json") as json_data:
        data = json.load(json_data)

    i = 0
    output = []

    for x in range(len(data)):
        relations(data[i])
        parseRel()
        with open("relations.json") as relData:
            output.append(json.load(relData))
        i += 1
        print(round(i / len(data) * 100, 1), "% Complete")
        relOutput = json.dumps(output, indent=4)
        with open("all_rel.json", "w") as out_file:
            out_file.write(relOutput)
        os.remove("relations.json")


def idChecker():

    with open("relations_filtered.json") as rel_data:
        relData = json.load(rel_data)

    with open("planning.json") as plan_data:
        planData = json.load(plan_data)

    r = 0
    p = 0

    tr = len(relData)

    output = []

    for x in range(len(relData) * len(planData)):
        if relData[r] == planData[p]["media"]["id"]:
            print(relData[r], "is a match")

            planData[p]["media"]["pfactor"] = 0.1

            output.append(planData[p]["media"])

            r = 0
            p += 1

        if r != tr:

            if relData[r] != planData[p]["media"]["id"]:

                #print(relData[r], "against", planData[p]["media"]["id"])

                r += 1

        if r == tr:

            planData[p]["media"]["pfactor"] = 0

            output.append(planData[p]["media"])

            r = 0
            p += 1

        if p == len(planData):

            planOutput = json.dumps(output, indent=4)

            print(planOutput, file=open("p_planning.json", "w"))

            break