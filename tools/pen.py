#################################################################
# FILE : pen.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - Pen Class
#################################################################
import tkinter as tk
import typing

from shape_attributes import ShapeAttributes


class Pen:
    """This is the Pen tool in the Paint program. Has attributes:
    1. Canvas - The space on which the cursor input is received from, and
    the area on which the "ink" is painted.
    2. Color of the pen
    3. Size of the pen
    """

    def __init__(self, canvas: tk.Canvas, shape_attributes: ShapeAttributes, color: typing.Optional[str] = None,
                 line_width: typing.Optional[int] = None,
                 last_x: int = 0, last_y: int = 0,
                 oval_list: typing.Optional[list[int]] = None,
                 oval_list_coords: typing.Optional[list[list[int]]] = None):

        # Set the main attributes of the pen
        self.canvas = canvas
        self.shape_attributes = shape_attributes
        self.color = color
        self.line_width = line_width

        # Set the drawing attribute to False, and create a position variable
        self.drawing_state: bool = False
        self.last_x = last_x
        self.last_y = last_y

        # A list of all the ovals created by the pen, and a list of their coordinates [x, y, x, y]
        self.oval_list = oval_list or []
        self.oval_list_coords = oval_list_coords or []

    def __eq__(self, other: int):
        """This method is used to determine if the tag of self is equal to another tag"""
        return other in self.oval_list

    def start_drawing(self, event) -> None:
        """This method turns drawing state to True when MB1 is pressed"""
        # Set the starting coordinates of the drawing
        x1, y1 = (event.x - 1), (event.y - 1)
        # Set pen drawing state to True
        self.drawing_state = True
        self.last_x, self.last_y = x1, y1

    def draw_with_antialiasing(self, x1: int, y1: int, x2: int, y2: int,
                               color: str, line_width: int) -> None:
        """This function makes the drawing of the pen smoother using antialiasing
        technique"""
        # Calculate the number of segments drawn according to the max difference in
        # x or y. Division by 2 determines the number of segments.
        num_segments = int(max(abs(x2 - x1), abs(y2 - y1)) / 2)
        # Ensure a minimum of one segment to prevent division by 0
        if num_segments == 0:
            num_segments = 1
        for i in range(num_segments + 1):
            ratio = i / num_segments
            x = int(x1 + ratio * (x2 - x1))
            y = int(y1 + ratio * (y2 - y1))
            # Create a line using tiny circles according to pen size.
            # The divisions by 2 make the line look more like a circle.
            self.oval_list.append(self.canvas.create_oval(x - line_width // 2, y - line_width // 2,
                                                          x + line_width // 2, y + line_width // 2,
                                                          fill=color, outline=color, width=line_width))
            new_oval_coords = [x - line_width // 2, y - line_width // 2,
                               x + line_width // 2, y + line_width // 2]
            self.oval_list_coords.append(new_oval_coords)

    def draw(self, event=None) -> None:
        """This function draws a free line on the canvas"""
        if event is None:
            # When drawing not from an event, we need to update the list so that
            # the new object treat all ovals as oval_list and not many ovals
            updated_oval_list = []
            for i in range(len(self.oval_list)):
                oval_coords = self.oval_list_coords[i]
                x0, y0, x1, y1 = oval_coords
                updated_oval_list.append(self.canvas.create_oval(x0, y0, x1, y1, fill=self.color,
                                                                 outline=self.color,
                                                                 width=self.line_width))
            self.oval_list = updated_oval_list
        if self.drawing_state:
            # Get the current x and y from mouse event
            x2, y2 = event.x, event.y
            # Get color and line width from shape attributes
            self.color = self.shape_attributes.get_color()
            self.line_width = self.shape_attributes.get_line_width()
            # Use the antialiasing drawing to draw
            self.draw_with_antialiasing(self.last_x, self.last_y, x2, y2,
                                        self.color, self.line_width)
            self.last_x, self.last_y = x2, y2

    def stop_drawing(self, event) -> None:
        """This function turns the drawing state back to False when Mouse Button 1 is released"""
        self.drawing_state = False

    def save_to_dict(self):
        """This method saves the data of a drawn pen to the dictionary"""
        # Save the data of the pen to the dictionary
        pen_dict = {"type": "pen",
                    "data": {"shape_attributes": {"color": self.shape_attributes.get_color(),
                                                  "scale_var": self.shape_attributes.get_line_width()},
                             "color": self.color,
                             "line_width": self.line_width,
                             "last_x": self.last_x,
                             "last_y": self.last_y,
                             "oval_list": self.oval_list,
                             "oval_list_coords": self.oval_list_coords}
                    }
        return pen_dict

    @classmethod
    def load_from_dict(cls, pen_dict: dict, canvas: tk.Canvas) -> object:
        # Get the info from pen_dict

        # Create a shape attribute object
        raw_shape_attributes = pen_dict["data"].pop("shape_attributes")
        scale_var = tk.IntVar()
        scale_var.set(raw_shape_attributes["scale_var"])
        shape_attributes = ShapeAttributes(color=raw_shape_attributes["color"],
                                           scale_var=scale_var)

        # Create a new pen
        new_pen = cls(canvas=canvas, shape_attributes=shape_attributes, **pen_dict["data"])
        return new_pen
