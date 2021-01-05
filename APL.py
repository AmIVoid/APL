import json

from pFactor import getPFactorData

# from sheets import sheets


def APL():

    user = input("AniList username: ")
    sheetId = input("Google Sheets ID: ")

    p_factor_data = getPFactorData(user)

    planOutput = json.dumps(p_factor_data, indent=4)
    with open("p_planning.json", "w") as out_file:
        out_file.write(planOutput)

    # sheets(sheetId)


APL()