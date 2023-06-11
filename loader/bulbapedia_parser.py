from abc import ABC
import requests
from bs4 import BeautifulSoup
from data.pokemon import Pokemon


class Parser(ABC):

    def __init__(self, link):
        self.link = link


class PokemonParser(Parser):

    def __init__(self, link):
        super().__init__(link)

    def handle_get_pokemon(self, pokemon_name):
        print("")


class ListParser(Parser):

    def __init__(self, link):
        super().__init__(link)

    # Function used to scrap the pokemon data out of the generation table
    # Return - a list of pokemon data from the table

    @staticmethod
    def download_img(img, pokemon_name):
        fname = pokemon_name + ".png"
        path = 'C:\\Users\\milos\\Kodowisko\\PJATK\\PPY\\Pokedex\\data\\images\\' + fname

        if img.startswith('//'):
            response = requests.get('https:' + img)

        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to Download Image")

        return path

    @staticmethod
    def process_generation(t_content):
        rows = t_content.find_all("tr")
        pkmn_list = []

        prev_national_number = None
        rowspan = None
        for row in rows[1:]:
            cells = row.find_all("td")
            if rowspan is None:
                rowspan_val = cells[0].get('rowspan')
                if rowspan_val is not None:
                    rowspan = int(rowspan_val)
                else:
                    rowspan = None
                national_number = cells[0].text.strip()
                name = cells[2].get_text(separator=' ')
                img = ListParser.download_img(cells[1].img['src'], name)
                types = [cell.text.strip() for cell in cells[3:]]
            else:
                national_number = prev_national_number
                name = cells[1].get_text(separator=' ')
                img = ListParser.download_img(cells[0].img['src'], name)
                types = [cell.text.strip() for cell in cells[2:]]

            rowspan -= 1
            if rowspan == 0:
                rowspan = None
            prev_national_number = national_number

            pkmn_list.append(Pokemon(national_number, name, types, img))
            print(f"{national_number}: {name} {types}")
        return pkmn_list

    # Function which handles getting pokemon table content and feeds it to process_generation()
    # Return - full list of all available pokemon
    def handle_get_pokemons(self):
        html = requests.get(self.link)
        soup = BeautifulSoup(html.content, "html.parser")
        full_list = []

        tables = soup.find_all("table", class_="roundy")
        i = 1
        for table in tables:
            full_list.append(self.process_generation(t_content=table))

        return full_list
