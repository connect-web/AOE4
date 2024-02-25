from bs4 import BeautifulSoup
import pandas as pd
import os
import json

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

def load_build_order(build_name="HRE Fast Castle.bo"):
    with open(os.path.join('build_orders', build_name), 'r', encoding='utf-8') as x:
        content = json.loads(x.read())
    """
    >Time (MM:SS)</th>
              <th>Description</th>
              <th>Food</th>
              <th>Wood</th>
              <th>Gold</th>
              <th>Stone</th>
    """
    headers = ['Time', 'Description', 'Food', 'Wood', 'Gold', 'Stone']
    data = []
    for each in content["build_order"]:

        data.append(
            (each.get('time') ,
             "\n".join(each['notes']) ,
             each['resources']['food'],
             each['resources']['wood'],
             each['resources']['gold'],
             each['resources']['stone']
             )
        )

    df = pd.DataFrame(data, columns=headers)
    return df