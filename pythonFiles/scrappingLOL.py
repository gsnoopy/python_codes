import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_champion_data(champion_name, role):
    champion_data = {}

    # Runas
    runas_data = set()
    url = f'https://u.gg/lol/champions/{champion_name}/build/{role}?rank=overall'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    active_perks1 = soup.find_all('div', class_='perk perk-active')
    active_perks2 = soup.find_all('div', class_='perk keystone perk-active')

    for active_perk in active_perks1 + active_perks2:
        imagens = active_perk.find_all('img')
        for img in imagens:
            runas_data.add(img['alt'])

    champion_data['runas'] = list(runas_data)

    # Stats
    shards_data = []
    shard_active_divs = soup.find_all('div', class_='shard shard-active')
    for shard_active_div in shard_active_divs:
        shard_image = shard_active_div.find('img')
        shard_name = shard_image['alt']
        shards_data.append(shard_name)

    shards_data = shards_data[:-3]  
    champion_data['stats'] = shards_data

    # Summoner Spells
    spells_data = set()
    for img in soup.find_all('img'):
        if 'spell' in img['src'] and 'Summoner' in img['src']:
            spells_data.add(img['alt'])
    champion_data['spells'] = list(spells_data)

    # Skill Order
    skills_data = []
    div_skill_priority_path = soup.find('div', class_='skill-priority-path')
    if div_skill_priority_path:
        skills_labels = div_skill_priority_path.find_all('div', class_='skill-label bottom-center')
        for label in skills_labels:
            skills_data.append(label.text.strip())
    champion_data['skill_order'] = skills_data

    # Counters
    counters_data = []
    div_matchups_toughest = soup.find('div', class_='matchups', id='toughest-matchups')
    if div_matchups_toughest:
        champion_names = div_matchups_toughest.find_all('div', class_='champion-name')
        for champion_name in champion_names:
            counters_data.append(champion_name.text.strip())
    champion_data['counters'] = counters_data

    return champion_data

def get_champion_items(champion_name):
    items_data = []
    url = f'https://probuildstats.com/champion/{champion_name}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_='item')
    for item in items:
        item_name = item.find('img')['alt']
        if not item_name.startswith('Summoner'):
            pick_rate = int(item.find('div', class_='pick-rate').get_text(strip=True).replace('%', ''))
            if pick_rate >= 15:
                items_data.append({'item': item_name, 'pick_rate': f"{pick_rate}%"})
    return items_data

@app.route('/champion_data', methods=['POST'])
def champion_data():
    champion_name = request.json.get('champion_name')
    role = request.json.get('role')

    if champion_name is None or role is None:
        champion_name = request.form.get('champion_name')
        role = request.form.get('role')

    if champion_name is None or role is None:
        return jsonify({'error': 'Nome do campeão ou papel não fornecido'}), 400

    champion_data = get_champion_data(champion_name, role)
    champion_data['items'] = get_champion_items(champion_name)
    return jsonify(champion_data)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=False)
