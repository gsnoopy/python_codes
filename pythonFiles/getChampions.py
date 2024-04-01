import requests
import json

def get_champion_info(url):
    response = requests.get(url)
    data = response.json()
    champions = data['data']
    
    champion_info = []
    for champ_name, champ_data in champions.items():
        champion_info.append({
            'name': champ_data['name'],
            'alias': champ_name,
            'splash': f"https://ddragon.leagueoflegends.com/cdn/14.5.1/img/champion/{champ_name}.png"
        })
    
    return champion_info

def save_champion_info(champion_info, filename):
    with open(filename, 'w') as f:
        json.dump(champion_info, f, indent=4)

if __name__ == "__main__":
    url = 'https://ddragon.leagueoflegends.com/cdn/14.5.1/data/en_US/champion.json'
    champion_info = get_champion_info(url)
    save_champion_info(champion_info, 'champion_info.json')
