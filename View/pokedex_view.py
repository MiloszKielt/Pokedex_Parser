import sys
import tkinter as tk
from tkinter import ttk
import json
import re


class Pokedex:
    """ @class: Pokedex
        @brief: This class displays the GUI of a pokedex to the user
        @details: The class implements functionalities like searching for a
                 specific pokemon or changing between the generations

        @param pokemon_gens: List of pokemons unloaded from the pokemon.json file
        @param window: Window which is the main display window for the app
        @param frm_main: Frame in which user specifies the generation
        @param frm_gen_view: Frame in which user browses through the pokemons
        @param user_input: Input of a user in the search field
    """

    def __init__(self, file_name):
        """ @param file_name: Name of file from which the data should be unpacked
            @return: An initialized instance of pokedex class with specified filename
        """
        try:
            self.pokemon_gens = self.unpack_content_json(file_name)
        except FileNotFoundError as e:
            print(f"file {e.filename} has not been found...")
            print("The Pokemon data has not been loaded, please load the data before execution."
                  "\nAborting execution...")
            sys.exit(-1)
        else:
            print("Initiating the pokedex...")

        self.pokemon_images = {}
        self.treeview = None
        self.window = tk.Tk()
        self.window.geometry("600x400")
        self.frm_main = tk.Frame(master=self.window)
        self.frm_main.pack()
        self.btn_type_chart = tk.Button(master=self.frm_main, command=self.switch_to_type_chart, text='Check type charts')
        self.btn_type_chart.pack()

        self.frm_type_chart = tk.Frame(master=self.window)
        self.type_chart_img = tk.PhotoImage(file="data/images/type_chart.png", master=self.frm_type_chart)
        self.frm_type_chart.pack()

        lbl_welcome = tk.Label(
            text="Choose Generation",
            font='Arial',
            master=self.frm_main
        )
        lbl_welcome.pack(pady=20)

        frm_btns = tk.Frame(master=self.frm_main)
        frm_btns.pack()

        i = 0
        j = 0
        for generation, pokemon in self.pokemon_gens.items():
            frm_btn = tk.Frame(master=frm_btns, relief=tk.RAISED, borderwidth=1)
            frm_btn.grid(row=j % 3, column=i % 3, padx=2, pady=2)
            btn_gen = tk.Button(text='Generation ' + generation, width=15, height=5, master=frm_btn,
                                command=lambda gen=generation: self.switch_to_gen_view(gen))
            btn_gen.pack()
            i += 1
            j += 1 if i % 3 == 0 else 0

        self.frm_gen_view = tk.Frame(master=self.window)
        self.user_input = tk.StringVar()

        self.frm_main.pack()

    @staticmethod
    def unpack_content_json(file_name):
        """ @desc: This method is used to unpack the content of the .json file containing
                   pokemon data
            @param file_name: Name of file from which the data should be unpacked
            @return: Pokemon data split between their generations
        """
        with open(file_name, 'r') as poke_file:
            generations = json.load(poke_file)

        return generations

    def go_back_to_menu(self):
        """ @desc: This method is used to go back to view of generation choice
        """
        self.frm_gen_view.pack_forget()
        self.frm_type_chart.pack_forget()
        self.user_input = tk.StringVar()
        self.window.geometry("600x400")
        self.frm_main.pack(fill='both', expand=1)

    def switch_to_gen_view(self, gen_num):
        """ @desc: This method is used to switch from the main menu to generation browsing
            @param gen_num: Number of generation which the user wants to browse
        """
        self.frm_main.pack_forget()
        self.update_gen_view(gen_num)
        self.window.geometry("600x1200")
        self.frm_gen_view.pack(fill='both', expand=1)

    def switch_to_type_chart(self):
        """ @desc: Method to switch between main menu view and type chart view
        """
        self.frm_main.pack_forget()
        self.window.geometry("1000x480")
        label = tk.Label(image=self.type_chart_img, master=self.frm_type_chart)
        label.pack()
        button_back = tk.Button(text="go back", command=self.go_back_to_menu, master=self.frm_type_chart)
        button_back.pack()
        self.frm_type_chart.pack(fill='both', expand=1)

    def search(self, gen_num):
        """ @desc: This method searches the generation list in order to find matching
                   pokemon
            @param gen_num: Number of generation to be searched
        """
        text = self.user_input.get()
        pkmn_search_list = self.pokemon_gens[gen_num]
        found = []
        for pokemon in pkmn_search_list:
            if re.match(text, pokemon['name'], re.IGNORECASE):
                found.append(pokemon)

        return found

    def update_gen_view(self, gen_num):
        """ @desc: Method used to update the view of the generation's pokemon list
            @param gen_num: Number of generation
        """
        for widget in self.frm_gen_view.winfo_children():
            widget.destroy()

        frm_top = tk.Frame(master=self.frm_gen_view)
        frm_top.pack()

        btn_back = tk.Button(
            text='Go Back',
            master=frm_top,
            command=self.go_back_to_menu
        )
        btn_back.pack(side=tk.LEFT, padx=10)

        lbl_gen = tk.Label(
            text="Generation " + gen_num,
            font='Arial',
            master=frm_top
        )
        lbl_gen.pack(pady=20, side=tk.LEFT)

        entry_search = tk.Entry(
            master=frm_top,
            textvariable=self.user_input
        )

        btn_search = tk.Button(
            master=frm_top,
            text='search',
            command=lambda gen=gen_num: self.update_gen_view(gen_num)
        )

        btn_search.pack(side=tk.RIGHT)
        entry_search.pack(side=tk.RIGHT)

        style = ttk.Style(self.frm_gen_view)
        style.configure("Pokemon.Treeview", rowheight=75)

        self.treeview = ttk.Treeview(self.frm_gen_view, style="Pokemon.Treeview")

        self.treeview['columns'] = ('Number', 'Name', 'Types')

        self.treeview.heading('#0', text='Image')
        self.treeview.heading('Number', text='National Number')
        self.treeview.heading('Name', text='Name')
        self.treeview.heading('Types', text='Types')

        self.treeview.column('#0', width=200)
        self.treeview.column('Number', width=100)
        self.treeview.column('Name', width=175)
        self.treeview.column('Types', width=200)

        if self.user_input.get() == '':
            pkmn_list = self.pokemon_gens[gen_num]
        else:
            pkmn_list = self.search(gen_num)

        for pokemon in pkmn_list:
            number = pokemon['number']
            name = pokemon['name']
            ptypes = pokemon['types']
            img_file_location = pokemon['img']
            image = tk.PhotoImage(file=img_file_location)
            self.pokemon_images[img_file_location] = image
            self.treeview.insert('', tk.END, text='', values=(number, name, ptypes), image=image)

        self.treeview.pack(fill=tk.BOTH, expand=True)
