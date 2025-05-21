#################################################################
# FILE : pixel.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - Pixel Class
#################################################################


class Pixel:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, size: int,
                 color: str, tag: int):
        # Set position
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        # Set attributes
        self.size = size
        self.color = color

        # Set the tag of the pixel
        self.tag = tag

    def set_tag(self, new_tag: int):
        self.tag = new_tag

    def save_to_dict(self) -> dict:
        """This method saves the data of a pixel to a dictionary"""
        # Save the data of the pixel to the dictionary
        pixel_dict = {"x1": self.x1,
                      "y1": self.y1,
                      "x2": self.x2,
                      "y2": self.y2,
                      "size": self.size,
                      "color": self.color,
                      "tag": self.tag}
        return pixel_dict

    @classmethod
    def load_from_dict(cls, pixel_dict: dict) -> object:
        """This method creates a pixel from a dictionary"""
        new_pixel = cls(**pixel_dict)
        return new_pixel

