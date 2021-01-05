import json
import requests
from ratelimit import limits, sleep_and_retry
import os
import time

RATE_LIMIT = 60
CALLS = 90


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def relations(listId):
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

    text_out = response.text

    with open("rel.json", "w") as out_file:
        out_file.write(text_out)


def parseRelations():
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


def relFilter():
    output = []

    with open("all_rel.json") as jsonData:
        relData = json.load(jsonData)

    output = [x["id"] for j in relData if j != [] for x in j]

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
        parseRelations()
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

                # print(relData[r], "against", planData[p]["media"]["id"])

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


def filterList(name):
    output = []

    with open("{}.json".format(name)) as jsonData:
        data = json.load(jsonData)

    for x in range(len(data)):
        output.append(data[x]["media"]["id"])

    objects = json.dumps(output, indent=4)

    with open("{}_filtered.json".format(name), "w") as out_file:
        out_file.write(objects)