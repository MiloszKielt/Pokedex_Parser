from View.pokedex_view import Pokedex

if __name__ == '__main__':
    fname = "data/pokemon.json"
    dex = Pokedex(fname)
    dex.window.mainloop()
