from bulbapedia_parser import PokemonParser
import json

# link to the wiki of pokemon list
list_link = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number'


def load_pokemons():
    """ @desc: Function used to load the pokemon data from the website to the
               .json file
    """
    pkmn_parser = PokemonParser(list_link)
    pokemon_list = pkmn_parser.handle_get_pokemons()
    i = 1

    generations = {}

    for generation in pokemon_list:
        generations[str(i)] = generation
        i += 1

    json_gens = {}
    for generation, pokemons in generations.items():
        json_pokemon = []
        for pokemon in pokemons:
            json_pokemon.append({
                'number': pokemon.number,
                'name': pokemon.name,
                'types': pokemon.ptypes,
                'img': pokemon.img
            })
        json_gens[generation] = json_pokemon

    with open("../data/pokemon.json", 'w') as file:
        json.dump(json_gens, file)


if __name__ == '__main__':
    load_pokemons()
