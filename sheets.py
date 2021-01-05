from pygsheetsorm import Repository, Model
import json

service_account_file = "./my-creds.json"

def sheets(sheetsId):
        
        repo = Repository.get_repository_with_creds(service_account_file=service_account_file, 
                                                    spreadsheet_id=sheetsId,
                                                    sheet_name="Raw Data")

        list = repo.get_all()

        with open("p_planning.json") as json_data:
                data = json.load(json_data)
                
        i = 0
        
        for x in range(len(data)):
        
            animeName = list[i]
        
            animeName.alt_name = data[i]["title"]["romaji"]
            animeName.episodes = data[i]["episodes"]
            animeName.episode_time = data[i]["duration"]
            animeName.mean_score = data[i]["averageScore"]
            animeName.anilist_id = data[i]["id"]
            animeName.p_factor = data[i]["pfactor"]
        
            animeName.Save()
        
            i += 1