import json

def parseFunc():
    with open('planning.json') as json_data:
        data = json.load(json_data)

    parsed = data["data"]["MediaListCollection"]["lists"][0]["entries"]

    for element in parsed: 
        del element['status']

    objects = json.dumps(parsed)

    with open('parsed.json', 'w') as out_file:
            out_file.write(objects)