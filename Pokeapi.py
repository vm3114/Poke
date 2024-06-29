import requests
import sys

def get_pokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}/"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print("Pokemon not found!")
            return None
        
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


def download_sprite(url, save_as):
    response = requests.get(url)

    with open(save_as, 'wb') as file:
        file.write(response.content)
        print("\nImage Downloaded!")


def name_format(name):
    modified = name.lower().replace("é", "e").replace(".", "").replace(" ", "-").replace("'", "").replace(":", "") # For pokemon with spaces in their names, Flabébé, Mr. Mime and Farfetch'd lines, and Type: Null 
    return modified


n = len(sys.argv)

if n == 2:
    pokemon = name_format(sys.argv[1])

else:
    name = " ".join(sys.argv[i] for i in range(1, n))
    pokemon = name_format(name)

data = get_pokemon(pokemon)
if data:
    print(f"\nName: {data['name'].capitalize()}")
    print(f"National Number: {data['id']}")

    print("Type(s):", end = ' ')
    types = ", ".join(slot["type"]["name"].capitalize() for slot in data["types"])
    print(types)

    print("Abilities:", end = ' ')
    abilities = ", ".join(slot["ability"]["name"].replace("-", " ").title() for slot in data["abilities"])
    print(abilities)
    
    print(f"Height: {data['height']/10} m")
    print(f"Weight: {data['weight']/10} kg")

    print("\nBase Stats:")
    total = 0
    for slot in data["stats"]:
        print(f"{slot['stat']['name'].replace('hp', 'HP').replace('-', ' ').capitalize()}: {slot['base_stat']}")
        total = total + slot['base_stat']
    print(f"Stat Total: {total}")

    sprite = data["sprites"]["other"]["official-artwork"]["front_default"]
    save_as = f"sprite.png"
    download_sprite(sprite, save_as)