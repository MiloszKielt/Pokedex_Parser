
class Pokemon:
    """ @class: Pokemon
        @brief: This class stores pokemon data
        @details: This class is used for saving the pokemon data into the .json file
    """

    def __init__(self, number, name, ptypes, img):
        """ @param number: National number of a pokemon
            @param name: name of a pokemon
            @param ptypes: types of the pokemon
            @param img: address of the image of pokemon
            @return Initialized object of Pokemon class
        """
        self.number = number
        self.name = name
        self.ptypes = ptypes
        self.img = img

    def get_type(self):
        """ @return: types of this pokemon
        """
        return self.ptypes

    def get_name(self):
        """ @return: name of this pokemon
        """
        return self.name

    def get_img(self):
        """ @return: path to the image of this pokemon
        """
        return self.img
