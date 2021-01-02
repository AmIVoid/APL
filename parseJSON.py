import json
import os


def parseFunc():
    with open("planning.json") as json_data:
        data = json.load(json_data)

    parsed = data["data"]["MediaListCollection"]["lists"][0]["entries"]

    for element in parsed:
        del element["status"]

    parse_format = [x for x in parsed if x["media"]["format"] == "TV"]

    parse_status = [x for x in parse_format if x["media"]["status"] == "FINISHED"]

    objects = json.dumps(parse_status, indent=4)

    with open("parsed.json", "w") as out_file:
        out_file.write(objects)

    os.remove("planning.json")
