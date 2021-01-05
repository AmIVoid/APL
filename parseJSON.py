import json
import os


def parseFunc(data):
    objects = json.loads(data)
    parsed = objects["data"]["MediaListCollection"]["lists"][0]["entries"]

    for element in parsed:
        del element["status"]

    parse_format = [x for x in parsed if x["media"]["format"] == "TV"]

    parse_status = [x for x in parse_format if x["media"]["status"] == "FINISHED"]

    return parse_status