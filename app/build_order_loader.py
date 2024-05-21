from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import re

def select_build_order_file():
    BO_files = {
        "1": 'French 3 38 Feudal All-in_Castle Timing.bo',
        "2": 'Ayyubids desert raider opening into FC by VortiX.bo',
        "3": "Beastyqt mongol kashik.bo",
        "4": "Zhu Xi's Legacy Fast Aggression [ Beasty ].bo",
        "5": "Rus 2 TC.bo"
    }
    for number, name in BO_files.items():
        print(f'[{number}] {name}')
    selected = input("Enter your choice:")
    while BO_files.get(selected) is None:
        print("\n Invalid choice. Please try again.")
        selected = input("Enter your choice:")

    df = load_build_order_file(BO_files.get(selected))
    return df


def get_dataframe(filename = 'ottomans_1.html'):
    with open(os.path.join('pages',filename), 'r', encoding='utf-8') as x:
        tableHtml = x.read()

    soup = BeautifulSoup(tableHtml, 'html.parser')

    table = soup.find('table')
    headers = table.find_all('th')
    headers = [header.text for header in headers]

    data = []
    for row in table.find_all('tr')[2:]:
        cells = row.findAll('td')
        if cells:
            cell_data = [cell.text.strip() for cell in cells]
            data.append(dict(zip(headers, cell_data)))

    df = pd.DataFrame(data, columns=headers)
    return df

def load_build_order_file(build_name="HRE Fast Castle.bo"):
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
        description = convert_to_html("\n".join(each['notes']))

        data.append(
            (each.get('time') ,
             description,
             each['resources']['food'],
             each['resources']['wood'],
             each['resources']['gold'],
             each['resources']['stone']
             )
        )

    df = pd.DataFrame(data, columns=headers)
    return df

def convert_to_html(text):
    # Use a regular expression to find all occurrences of @<path>@
    # and replace them with <img src='<path>'>
    # The pattern looks for '@', followed by any character that is not '@' (non-greedy), followed by '@'
    # and replaces it with <img src='...'>

    # html_text = re.sub(r'@([^@]+)@', r"<img src='./pictures/\1' width='50' height = '50'>", text)
    html_text = re.sub(r'@([^@]+)@', replacement_function, text)
    return html_text

def replacement_function(match):
    file_path = match.group(1)  # Get the matched file path

    # Extract the alt text by splitting the file path and taking the last part before '.png'
    alt_text = file_path.split('/')[-1].split('.png')[0]
    # Return the <img> tag with the src set to the file path, and the alt attribute set to the extracted alt text
    image_inline = f"<img src='./pictures/{file_path}' width='50' height='50' alt='{alt_text}' title='{alt_text}'>"
    return image_inline + f' {alt_text}'.replace("-", " ") if 'landmark_' in file_path else image_inline

