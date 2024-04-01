import requests
import json

def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to download JSON from {url}")
        return None

def merge_translations(en_json, pt_json):
    merged_json = []

    for key in en_json["data"]:
        en_translation = en_json["data"][key]["name"]
        pt_translation = pt_json["data"][key]["name"]

        merged_json.append({
            "en_us": en_translation,
            "pt_br": pt_translation
        })

    return merged_json

def main():
    en_url = "https://ddragon.leagueoflegends.com/cdn/14.5.1/data/en_US/item.json"
    pt_url = "https://ddragon.leagueoflegends.com/cdn/14.5.1/data/pt_BR/item.json"

    en_json = download_json(en_url)
    pt_json = download_json(pt_url)

    if en_json and pt_json:
        merged_translations = merge_translations(en_json, pt_json)

        with open("itens.json", "w") as f:
            json.dump(merged_translations, f, indent=4)
        
        print("Merged translations saved to 'itens.json'")

if __name__ == "__main__":
    main()
