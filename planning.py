import requests
import os
import json
from ratelimit import limits, sleep_and_retry
from parseJSON import parseFunc

RATE_LIMIT = 60
CALLS = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def search(search):
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