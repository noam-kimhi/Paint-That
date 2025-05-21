#################################################################
# FILE : triangle.py
# WRITER : Noam Kimhi, noam.kimhi
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - Triangle Class
#################################################################
import tkinter as tk
import typing
import uuid

from shape_attributes import ShapeAttributes


class Triangle:
    """This is the Triangle Tool in the Paint program. Has attributes:
        1. Canvas - The space on which the cursor input is received from, and
        the area on which the Triangle is painted.
        2. Color of the triangle
        3. Line width of the triangle
        """

    def __init__(self, canvas: tk.Canvas, shape_attributes: ShapeAttributes, color: typing.Optional[str] = None,
                 line_width: typing.Optional[int] = None,
                 fill_color: str = "", last_x: int = 0, last_y: int = 0,
                 x: typing.Optional[int] = None, y: typing.Optional[int] = None):

        # Set the main attributes of the triangle
        self.canvas = canvas
        self.shape_attributes = shape_attributes
        self.color = color
        self.line_width = line_width
        self.fill_color = fill_color

        # Set the position of the triangle
        self.last_x = last_x
        self.last_y = last_y
        self.x = x
        self.y = y

        # generate a random id for the triangle
        self.tag: str = str(uuid.uuid4())

        # Set the drawing attribute to False
        self.drawing_state: bool = False

    def __eq__(self, other: int) -> bool:
        """This method is used to determine if the tag of self is equal to another tag"""
        return self.tag == other

    def start_drawing(self, event) -> None:
        # Set the starting coordinates of the drawing
        x1, y1 = (event.x - 1), (event.y - 1)
        # Set drawing state to True
        self.drawing_state = True
        self.last_x, self.last_y = x1, y1

    def draw(self, event=None) -> None:
        if event is not None:
            # if shape is drawn by an event, get mouse events
            x, y = event.x, event.y
            self.x, self.y = x, y
            if self.drawing_state:
                self.canvas.delete(self.tag)
                self.color = self.shape_attributes.get_color()
                self.line_width = self.shape_attributes.get_line_width()
                self.draw_triangle(self.last_x, self.last_y, x, y, self.color, self.line_width)
        else:
            # else, draw shape from object attributes
            self.draw_triangle(self.last_x, self.last_y, self.x, self.y, self.color, self.line_width, self.fill_color)

    def stop_drawing(self, event) -> None:
        self.drawing_state = False

    def draw_triangle(self, x1: int, y1: int, x2: int, y2: int, color: str, line_width: int,
                      fill_color: str = "") -> None:
        self.tag = self.canvas.create_polygon(x1, y1, x2, y2, x2 + (x2 - x1), y1, fill=fill_color,
                                              outline=color,
                                              width=line_width)

    def save_to_dict(self) -> dict:
        """This method saves the data of a drawn triangle to the dictionary"""
        # Save the data of the triangle to the dictionary
        triangle_dict = {"type": "triangle",
                         "data": {"shape_attributes": {"color": self.shape_attributes.get_color(),
                                                       "scale_var": self.shape_attributes.get_line_width()},
                                  "color": self.color,
                                  "fill_color": self.fill_color,
                                  "line_width": self.line_width,
                                  "last_x": self.last_x,
                                  "last_y": self.last_y,
                                  "x": self.x,
                                  "y": self.y}
                         }
        return triangle_dict

    @classmethod
    def load_from_dict(cls, triangle_dict, canvas) -> object:
        # Get the info from triangle_dict

        # Create a shape attribute object
        raw_shape_attributes = triangle_dict["data"].pop("shape_attributes")
        scale_var = tk.IntVar()
        scale_var.set(raw_shape_attributes["scale_var"])
        shape_attributes = ShapeAttributes(color=raw_shape_attributes["color"],
                                           scale_var=scale_var)

        # Create a new triangle
        new_triangle = cls(canvas=canvas, shape_attributes=shape_attributes, **triangle_dict["data"])
        return new_triangle
