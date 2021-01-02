import json
import requests
from ratelimit import limits, sleep_and_retry
import os

RATE_LIMIT = 60
CALLS = 60


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

    i = 0

    while i <= len(parse_type):
        i += 1

    objects = json.dumps(parse_type, indent=4)

    with open("relations.json", "w") as out_file:
        out_file.write(objects)

    os.remove("rel.json")


def planFilter():
    with open("planning.json") as jsonData:
        planData = json.load(jsonData)

    output = []

    f = 0

    for x in range(len(planData)):
        print(planData[f])
        print(planData[f]["media"]["id"])
        output.append(planData[f]["media"]["id"])
        f +=1

    planObjects = json.dumps(output, indent=4)

    with open("planning_filtered.json", "w") as out_file:
        out_file.write(planObjects)

def runRel():
    with open("planning_filtered.json") as json_data:
        data = json.load(json_data)
    
    i = 0
    output = []
    
    for x in range(len(data)):
        relations(data[i])
        parseRel()
        with open("relations.json") as relData:
            output.append(json.load(relData))
        #print("AniList ID:", data[i])
        #print("Array index:", i)
        i +=1
        relOutput = json.dumps(output, indent=4)
        with open("all_rel.json", "w") as out_file:
            out_file.write(relOutput)