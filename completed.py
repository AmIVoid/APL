import requests
import os
from ratelimit import limits, sleep_and_retry
from parseJSON import parseFunc

RATE_LIMIT = 60
CALLS = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def completed_search(completed_search):
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

    text_out = response.text

    with open("output.json", "w") as out_file:
        out_file.write(text_out)


def getVars():
    return input("Anilist username: ")


if __name__ == "__main__":
    completed_search(getVars())

parseFunc()

if os.path.isfile("completed.json"):
    os.remove("completed.json")
    os.rename("parsed.json", "completed.json")
else:
    os.rename("parsed.json", "completed.json")