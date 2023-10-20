import csv


def updateSheets(p_factor_data):
    sorted_p_factor_data = sorted(
        p_factor_data, key=lambda x: x['APL'], reverse=True)

    with open('data.csv', 'w', newline='', encoding='utf-8') as data_file:
        csv_writer = csv.writer(data_file)
        count = 0
        for i in sorted_p_factor_data:
            i['title'] = i['title']['romaji']
            if count == 0:
                header = i.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(i.values())
