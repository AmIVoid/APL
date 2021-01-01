import requests
import json
from ratelimit import limits, sleep_and_retry

RATE_LIMIT = 60
CALLS = 60

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def search(search):
    # Here we define our query as a multi-line string
    query = '''
  query ($username: String, $type: MediaType, $status: MediaListStatus) {
    MediaListCollection(userName: $username, type: $type, status: $status) {
        lists {
            name
            entries {
                status
                media {
                    title { romaji }
                    episodes
                    duration
                    averageScore
                    format
                    id
              }
            }
          }
        }
      }
  '''

    # Define our query variables and values that will be used in the query request
    variables = {
        'username': search,
        'type': 'ANIME',
        'status': 'PLANNING'
    }

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})

    text_out = response.text

    with open('planning.json', 'w') as out_file:
        out_file.write(text_out)


def getVars():
  return input("Anilist username: ")


if __name__ == '__main__':
    search(getVars())