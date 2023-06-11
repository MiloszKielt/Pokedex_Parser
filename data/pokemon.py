
class Pokemon:

    def __init__(self, number, name, ptypes, img):
        self.number = number
        self.name = name
        self.ptypes = ptypes
        self.img = img

    def get_type(self):
        return self.ptypes

    def get_name(self):
        return self.name

    def get_img(self):
        return self.img
