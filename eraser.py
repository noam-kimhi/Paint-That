#################################################################
# FILE : eraser.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - Eraser Class
#################################################################
import tkinter as tk
import typing

from pen import Pen


class Eraser:
    """This is the eraser class. Used to delete shapes from the board"""

    def __init__(self, canvas: tk.Canvas, drawings_list, prev_drawings_list, size: tk.IntVar = None):
        # Set the main attributes of the eraser
        self.canvas: tk.Canvas = canvas
        self.eraser_size: tk.IntVar = size
        self.size = 0
        self.indicator = None
        self.drawings_list: list = drawings_list
        self.prev_drawings_list: list = prev_drawings_list

        # Set position variable
        self.prev_coords: typing.Optional[tuple[int, int]] = None

    def start_erasing(self, event):
        """This method defines the beginning of the erasing act"""
        # Get event x and y position
        x, y = event.x, event.y
        self.prev_coords = (x, y)
        # Create an eraser indicator
        self.eraser_indicator(x, y)

    def erase(self, event):
        """This function defines the act of erasing an object from the board"""
        self.size = self.eraser_size.get() * 5
        if self.prev_coords:
            x, y = event.x, event.y
            self.update_eraser_indicator(x, y)
            # Find overlapping items in a rectangle around the cursor
            overlapping_items = self.canvas.find_overlapping(x - self.size // 2,
                                                             y - self.size // 2,
                                                             x + self.size // 2,
                                                             y + self.size // 2)
            for item in overlapping_items:
                # Delete overlapping items, except the rectangle of the indicator
                if item != self.indicator:
                    shape_index = self.drawings_list.index(item)
                    # In case the shape is made by pen
                    if isinstance(self.drawings_list[shape_index], Pen):
                        pen_drawing = self.drawings_list[shape_index]
                        # remove the oval from oval_list in the pen drawing
                        pen_drawing.oval_list.remove(item)
                        # remove the oval coordination from oval_list in the pen drawing
                        item_coords = self.canvas.coords(item)
                        self.drawings_list[shape_index].oval_list_coords.remove(item_coords)
                        # delete the oval
                        self.canvas.delete(item)
                        # If all ovals were deleted, remove the shape from drawing list
                        if len(pen_drawing.oval_list) == 0:
                            self.drawings_list.pop(shape_index)
                    else:
                        # delete the shape from the canvas
                        self.canvas.delete(item)
                        # remove the shape from drawing list
                        shape_to_remove = self.drawings_list.pop(self.drawings_list.index(item))
                        # add the shape to the prev drawings list
                        self.prev_drawings_list.append(shape_to_remove)
        event.x, event.y = self.prev_coords

    def stop_erasing(self, event):
        """This method is used to stop the erasing act"""
        # Remove the eraser indicator
        if self.indicator:
            self.canvas.delete(self.indicator)
        # Reset coordinates
        self.prev_coords = None

    def eraser_indicator(self, x, y):
        """Create an indicator for the current size and position of the eraser"""
        self.indicator = self.canvas.create_rectangle(x - self.size // 2, y - self.size // 2,
                                                      x + self.size // 2, y + self.size // 2,
                                                      outline='#e67eb8', fill='pink', width="2", dash=(2, 2))

    def update_eraser_indicator(self, x, y):
        """Update the position of the eraser indicator"""
        # If an indicator exists -
        if self.indicator:
            # set the coordinates of the indicator
            self.canvas.coords(
                self.indicator,
                x - self.size // 2, y - self.size // 2,
                x + self.size // 2, y + self.size // 2)
