#################################################################
# FILE : text.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - Text Class
#################################################################
import tkinter as tk
import typing
from tkinter import simpledialog

from shape_attributes import ShapeAttributes


class Text:
    """This is the Text Tool in the Paint program. Has attributes:
        1. Canvas - The space on which the cursor input is received from, and
        the area on which the oval is painted.
        2. Color of the text
        3. Size of the text
        """

    def __init__(self, canvas: tk.Canvas, shape_attributes: ShapeAttributes, text: str = "",
                 font: typing.Optional[tuple[str, int]] = None, color: typing.Optional[str] = None,
                 position: list[int] = None):
        # Set the main attributes of the text object
        self.canvas = canvas
        self.shape_attributes = shape_attributes
        self.tag: typing.Optional[int] = None
        self.text = text
        self.font = font
        self.color = color
        # If no position was given, place at [350, 350]
        self.position = position or [350, 350]

    def __eq__(self, other: int):
        """This method is used to determine if 2 shapes are the same"""
        return self.tag == other

    def draw(self) -> None:
        """This method defines the sequence of adding a new text to the canvas.
        It will ask the user for a text to add, the ask for a font and apply it with
        the current color"""
        # If text is an empty string, ask for text
        if not self.text:
            self.text = simpledialog.askstring("Add Text", "Enter your text:")
        # If there is a text input (meaning the user did not cancel) or text already exists
        if self.text:
            # Get the font from the user
            if self.font is None:
                self.font = self.choose_font()
            # Get the current color
            if self.color is None:
                self.color = self.shape_attributes.get_color()
            # If the user picked a font (did not cancel) or font already exists
            if self.font is not None and self.color is not None:
                # Add the text to the canvas
                self.tag = self.canvas.create_text(self.position, text=self.text,
                                                   font=self.font, fill=self.color)

    @staticmethod
    def choose_font() -> typing.Optional[tuple]:
        """This method gets the desired font style from the user"""
        # With simple dialog ask for a string representing the font
        selected_font = simpledialog.askstring("Choose Font", "Select a font:",
                                               initialvalue="Arial")
        # If got a font style, ask for font size
        if selected_font:
            font_size = simpledialog.askinteger("Choose Font Size", "Enter the font size:")
            # If got font size, return the selection, else return None
            if font_size:
                return selected_font, font_size
        return

    def save_to_dict(self) -> dict:
        """This method saves the data of a drawn text to the dictionary"""
        # Save the data of the text to the dictionary
        text_dict = {"type": "text",
                     "data": {"shape_attributes": {"color": self.shape_attributes.get_color(),
                                                   "scale_var": self.shape_attributes.get_line_width()},
                              "text": self.text,
                              "font": self.font,
                              "color": self.color,
                              "position": self.position}
                     }
        return text_dict

    @classmethod
    def load_from_dict(cls, text_dict: dict, canvas: tk.Canvas):
        # Get the info from text_dict

        # Create a shape attribute object
        raw_shape_attributes = text_dict["data"].pop("shape_attributes")
        scale_var = tk.IntVar()
        scale_var.set(raw_shape_attributes["scale_var"])
        shape_attributes = ShapeAttributes(color=raw_shape_attributes["color"],
                                           scale_var=scale_var)

        # Create new text
        new_text = cls(canvas=canvas, shape_attributes=shape_attributes, **text_dict["data"])
        return new_text
