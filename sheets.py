from pygsheetsorm import Repository, Model
import json

service_account_file = "credentials.json"

def updateSheets(sheetsId, sheetName, p_factor_data):

    repo = Repository.get_repository_with_creds(
        service_account_file=service_account_file,
        spreadsheet_id=sheetsId,
        sheet_name=sheetName,
    )

    list = repo.get_all()

    for i in range(len(p_factor_data)):

        animeName = list[i]

        animeName.alt_name = p_factor_data[i]["title"]["romaji"]
        animeName.episodes = p_factor_data[i]["episodes"]
        animeName.episode_time = p_factor_data[i]["duration"]
        animeName.mean_score = p_factor_data[i]["averageScore"]
        animeName.anilist_id = p_factor_data[i]["id"]
        animeName.p_factor = p_factor_data[i]["pfactor"]

        animeName.Save()
