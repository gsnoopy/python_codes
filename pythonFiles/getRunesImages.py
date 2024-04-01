import json
import requests
from bs4 import BeautifulSoup

urls = [
    'https://u.gg/lol/champions/zac/build',
    'https://u.gg/lol/champions/irelia/build',
    'https://u.gg/lol/champions/janna/build',
    'https://u.gg/lol/champions/rengar/build'
]

runes_dict = {}

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    rune_trees_container = soup.find('div', class_='rune-trees-container-2 media-query media-query_MOBILE_SMALL__MOBILE_MEDIUM')


    images = rune_trees_container.find_all('img')


    for img in images:
        runa_nome = img.get('alt')
        runa_link = img.get('src')
        

        if runa_nome not in runes_dict:
            runes_dict[runa_nome] = runa_link


with open('runes.json', 'w') as json_file:
    json.dump(runes_dict, json_file, indent=4)

print("Arquivo runes.json salvo com sucesso!")
