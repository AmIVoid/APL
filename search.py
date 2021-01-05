import requests
import os
import json
from ratelimit import limits, sleep_and_retry

RATE_LIMIT = 60
CALLS = 60


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

    response = requests.post(url, json={"query": query, "variables": variables})
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

    variables = {"username": completed_search, "type": "ANIME", "status": "COMPLETED"}

    url = "https://graphql.anilist.co"

    response = requests.post(url, json={"query": query, "variables": variables})
    parsed_response = parseFunc(response.text)

    return parsed_response


def parseFunc(data):
    objects = json.loads(data)
    parsed = objects["data"]["MediaListCollection"]["lists"][0]["entries"]

    for element in parsed:
        del element["status"]

    parse_format = [x for x in parsed if x["media"]["format"] == "TV"]

    parse_status = [x for x in parse_format if x["media"]["status"] == "FINISHED"]

    return parse_status