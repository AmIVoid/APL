import csv


def updateSheets(p_factor_data):
    sorted_p_factor_data = sorted(
        p_factor_data, key=lambda x: x['APL'], reverse=True)

    for row_num, i in enumerate(sorted_p_factor_data):
        del i['format']
        del i['status']
        i['Anime'] = '=HYPERLINK("https://anilist.co/anime/"&I' + \
            str(row_num+2)+', J'+str(row_num+2)+')'
        i['Watch Time'] = '=IF(C'+str(row_num+2) + \
            '=0,"",(C'+str(row_num+2)+'*D'+str(row_num+2)+'/60))'

    with open('data.csv', 'w', newline='', encoding='utf-8-sig') as data_file:
        csv_writer = csv.writer(
            data_file, quoting=csv.QUOTE_MINIMAL)
        count = 0
        for i in sorted_p_factor_data:
            i['title'] = i['title']['romaji']
            if count == 0:
                header = ['Anime', 'APL', 'episodes', 'duration', 'Watch Time',
                          'averageScore', 'pfactor', 'bfactor', 'id', 'title']
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow([str(i[column]) if column not in [
                                'Anime', 'Watch Time'] else i[column] for column in header])
