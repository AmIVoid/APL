import csv
import json
import pandas


def updateSheets(p_factor_data):
    with open('data.csv', 'w', newline='', encoding='utf-8') as data_file:
        csv_writer = csv.writer(data_file)
        count = 0
        for i in p_factor_data:
            if count == 0:
                header = i.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(i.values())
