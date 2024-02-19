from bs4 import BeautifulSoup
import pandas as pd
import os

def get_dataframe(filename = 'ottomans_1.html'):
    with open(os.path.join('pages',filename), 'r', encoding='utf-8') as x:
        tableHtml = x.read()

    soup = BeautifulSoup(tableHtml, 'html.parser')

    table = soup.find('table')
    headers = table.find_all('th')
    headers = [header.text for header in headers]

    done = {}

    data = []
    for row in table.find_all('tr')[2:]:
        cells = row.findAll('td')
        if cells:
            cell_data = [cell.text.strip() for cell in cells]
            data.append(dict(zip(headers, cell_data)))

    df = pd.DataFrame(data, columns=headers)
    return df