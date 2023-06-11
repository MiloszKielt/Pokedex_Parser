# Pokedex_Parser
The purpose of this program is to be able to check your favorite pokemon's types, names or looks.

REQUIRED LIBRARIES\DEPENDENCIES:
------------------------------------------------------------------
1. tkinter - necessary to provide GUI for the user
2. json - necessary for loading and saving data to files
3. beatifulsoup - necessary for scraping the data from bulbapedia.bulbagarden.net
4. re - needed to validate search input from user when searching for specified pokemon
5. requests - the program uses this library to access HTML content
------------------------------------------------------------------

HOW TO RUN:
------------------------------------------------------------------
-If you execute the program for the first time:
   1. Install all required packages
   2. Run the loader.py script located in 'loader' folder, which
      will load all required data for the program to run.
   3. Run main.py
   4. Enjoy!
-If you already loaded the data:
   1. Run main.py
   2. Enjoy!
------------------------------------------------------------------

KEY FEATURES:
------------------------------------------------------------------
  - Displaying to user Pokemon's image, name, number and types
  - Navigating through different pokemon generations
  - searching for specified pokemon in a generation
------------------------------------------------------------------

CHALLENGES FACED AND LESSONS LEARNED:
------------------------------------------------------------------
  - Correct management of filename addressing over different packages
     *learned that the access path is relevant from the context of file in which script was ran
  - Downloading and Presenting images inside GUI widgets
     *learned that images have problems with displaying if not stored as a variable somewhere
  - Stylizing components in tkinter for correct fitting of images inside widgets
     *learned about the ttk package of tkinter which allows for setting widget styles (through class Style) in a clearer and more reusable way,
      and also about it's different classes from which i used Treeview
------------------------------------------------------------------
