import sys
import tkinter as tk
from tkinter import ttk
import json
import re


def unpack_content_json(file_name):
    with open(file_name, 'r') as poke_file:
        generations = json.load(poke_file)

    return generations


class Pokedex:

    def go_back_to_menu(self):
        self.frm_gen_view.pack_forget()
        self.user_input = tk.StringVar()
        self.frm_main.pack(fill='both', expand=1)

    def switch_to_gen_view(self, gen_num):
        self.frm_main.pack_forget()
        self.update_gen_view(gen_num)
        self.frm_gen_view.pack(fill='both', expand=1)

    def search(self, gen_num):
        text = self.user_input.get()
        pkmn_search_list = self.pokemon_gens[gen_num]
        found = []
        for pokemon in pkmn_search_list:
            if re.match(text, pokemon['name'], re.IGNORECASE):
                found.append(pokemon)

        return found

    def update_gen_view(self, gen_num):
        for widget in self.frm_gen_view.winfo_children():
            widget.destroy()

        frm_top = tk.Frame(master=self.frm_gen_view)
        frm_top.pack()

        btn_back = tk.Button(
            text='Go Back',
            width=10,
            height=2,
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

        self.treeview['columns'] = ('Number', 'Name', 'Types', 'Image')

        self.treeview.heading('#0', text='Image')
        self.treeview.heading('Number', text='National Number')
        self.treeview.heading('Name', text='Name')
        self.treeview.heading('Types', text='Types')

        self.treeview.column('#0', width=200)
        self.treeview.column('Number', width=100)
        self.treeview.column('Name', width=150)
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

    def __init__(self, file_name):
        try:
            self.pokemon_gens = unpack_content_json(file_name)
        except FileNotFoundError as e:
            print("The Pokemon data has not been loaded, aborting execution")
            sys.exit(-1)
        
        self.pokemon_images = {}
        self.treeview = None
        self.window = tk.Tk()
        self.user_input = tk.StringVar()
        self.window.geometry("600x400")

        self.frm_main = tk.Frame(master=self.window)
        self.frm_main.pack()

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
            frm_btn = tk.Frame(
                master=frm_btns,
                relief=tk.RAISED,
                borderwidth=1
            )
            frm_btn.grid(row=i % 3, column=j % 3, padx=2, pady=2)
            i += 1
            j += 1 if i % 3 == 0 else 0

            btn_gen = tk.Button(
                text='Generation ' + generation,
                width=15,
                height=5,
                master=frm_btn,
                command=lambda gen=generation: self.switch_to_gen_view(gen)
            )
            btn_gen.pack()

        self.frm_gen_view = tk.Frame(master=self.window)

        self.frm_main.pack()
        self.window.mainloop()


if __name__ == '__main__':
    fname = "../data/pokemon.json"
    dex = Pokedex(fname)
