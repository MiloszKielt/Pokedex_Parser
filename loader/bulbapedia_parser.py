import requests
from bs4 import BeautifulSoup
from data.pokemon import Pokemon


class PokemonParser:
    """ @class: PokemonParser
        @brief: This class handles the web-scraping part of the app
        @details: This class through its methods allows the program to access the
                HTML content of the website through requests package and processes
                it with BeautifulSoup in order to provide resulting list and create
                appropriate image files

        @param link: A str containing link to the wiki website

    """
    def __init__(self, link):
        """ @param link: link to the wiki website
            @return: initialized object of PokemonParser class, with specified link to
                     the website
        """
        self.link = link

    @staticmethod
    def download_img(img, pokemon_name):
        """ @desc: This method handles downloading pokemon images from the web and saves
                   them in files
            @param img: url to the image
            @param pokemon_name:  name of pokemon appearing on the image
            @return: path to the image (sliced to be accessible from content root)
        """
        fname = pokemon_name + ".png"
        path = '..\\data\\images\\' + fname

        if img.startswith('//'):
            response = requests.get('https:' + img)
        else:
            response = requests.get(img)

        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to Download Image")

        return path[3:]

    @staticmethod
    def process_generation(t_content):
        """ @desc: Method used to create a list of Pokemon objects from the provided HTML
                   table
            @param t_content: content of the pokemon generation table
            @return: a list containing all pokemons from the generation
        """
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
                img = PokemonParser.download_img(cells[1].img['src'], name)
                types = [cell.text.strip() for cell in cells[3:]]
            else:
                national_number = prev_national_number
                name = cells[1].get_text(separator=' ')
                img = PokemonParser.download_img(cells[0].img['src'], name)
                types = [cell.text.strip() for cell in cells[2:]]

            rowspan -= 1
            if rowspan == 0:
                rowspan = None

            prev_national_number = national_number

            pkmn_list.append(Pokemon(national_number, name, types, img))
            print(f"{national_number}: {name} {types}")

        return pkmn_list

    def handle_get_pokemons(self):
        """ @desc: This method gets the html content and creates a list of
                   pokemon generations from it
            @return: A list containing all pokemon from all generations
        """
        html = requests.get(self.link)
        soup = BeautifulSoup(html.content, "html.parser")
        full_list = []

        tables = soup.find_all("table", class_="roundy")
        i = 1
        for table in tables:
            full_list.append(self.process_generation(t_content=table))

        return full_list
