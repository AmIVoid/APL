import requests
import json
import time
from ratelimit import limits, sleep_and_retry

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

    variables = {
        'id': listId
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.post(
        url, json={'query': query, 'variables': variables}, headers=headers)

    if response.status_code == 429:
        # retry after 5 seconds
        time.sleep(5)
        return getRelationsData(listId)

    response.raise_for_status()

    return json.loads(response.text)


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def planningSearch(search):
    query = """
	query($username: String, $type: MediaType, $status: MediaListStatus) {
    MediaListCollection(userName: $username, type: $type, status: $status) {
        lists {
            name
            entries {
                status
                media {
                    title {
                        romaji
                    }
                    episodes
                    duration
                    averageScore
                    format
                    status
                    id
                }
            }
        }
    }
}
	"""

    variables = {"username": search, "type": "ANIME", "status": "PLANNING"}
    url = "https://graphql.anilist.co"

    response = requests.post(
        url, json={"query": query, "variables": variables})
    parsed_response = parseFunc(response.text)

    return parsed_response


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def completedSearch(completed_search):
    query = """
	query($username: String, $type: MediaType, $status: MediaListStatus) {
    MediaListCollection(userName: $username, type: $type, status: $status) {
        lists {
            name
            entries {
                status
                media {
                    title {
                        romaji
                    }
                    format
                    status
                    id
                }
            }
        }
    }
}
	"""

    variables = {"username": completed_search,
                 "type": "ANIME", "status": "COMPLETED"}

    url = "https://graphql.anilist.co"

    response = requests.post(
        url, json={"query": query, "variables": variables})
    parsed_response = parseFunc(response.text)

    return parsed_response


def parseFunc(data):
    objects = json.loads(data)
    parsed = objects["data"]["MediaListCollection"]["lists"][0]["entries"]

    for element in parsed:
        del element["status"]

    allowed_formats = ["TV", "TV_SHORT"]
    parse_format = [x for x in parsed if x["media"]
                    ["format"] in allowed_formats]

    parse_status = [x for x in parse_format if x["media"]
                    ["status"] == "FINISHED"]

    return parse_status
