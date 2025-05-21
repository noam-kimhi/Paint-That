#################################################################
# FILE : pixel_pen.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - PixelPen Class
#################################################################
import tkinter
import tkinter as tk
import typing

from pixel import Pixel


class PixelPen:
    def __init__(self, canvas: tk.Canvas, left_color: str = "black",
                 right_color: str = "white", pixel_size: int = 20):
        self.canvas = canvas
        self.right_color = right_color
        self.left_color = left_color
        self.pixel_size = pixel_size

    def set_color(self, color: str, side: str) -> None:
        """
        This function sets up the left or right color of the pen, depending on
        the given side, to a desired color
        :param color: A string to which the color of the pen will be set
        :param side: "right" or "left"
        :return: None
        """
        if side == "right":
            self.right_color = color
        if side == "left":
            self.left_color = color

    def draw_pixel(self, event: tkinter.Event = None,
                   pixel: typing.Optional[object] = None) -> Pixel:
        """This function draws the pixels on the board."""
        if event is not None:
            # Set the color of the pixel according to which side was given
            if event.num == 1:
                pixel_color = self.left_color
            else:
                pixel_color = self.right_color

            # Ensure the position of the pixel is fixed in the grid
            x1 = event.x - event.x % self.pixel_size
            y1 = event.y - event.y % self.pixel_size
            x2 = x1 + self.pixel_size
            y2 = y1 + self.pixel_size

            pixel_tag = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                     fill=pixel_color, outline=pixel_color)
            # Create a new pixel object at the drawn location, with current size and color
            new_pixel = Pixel(x1, y1, x2, y2, self.pixel_size, pixel_color, pixel_tag)
            return new_pixel
        # If called not by an event, from a given pixel, create rectangle
        else:
            # create a new, updated tag for the pixel, and set it to him.
            pixel: Pixel
            new_tag = self.canvas.create_rectangle(pixel.x1, pixel.y1, pixel.x2, pixel.y2,
                                                   fill=pixel.color, outline=pixel.color)
            pixel.set_tag(new_tag)

    def draw_pixel_mirror(self, event: tkinter.Event = None) -> [Pixel, Pixel]:
        """This function draws a pixel at event location, and another one at
        the mirrored X position"""
        # Set the color of the pixel according to which side was given
        if event.num == 1:
            pixel_color = self.left_color
        else:
            pixel_color = self.right_color

        # Ensure the position of the pixel is fixed in the grid - Pixel 1
        x1 = event.x - event.x % self.pixel_size
        y1 = event.y - event.y % self.pixel_size
        x2 = x1 + self.pixel_size
        y2 = y1 + self.pixel_size

        # Get the position of the mirrored pixel
        canvas_width = 32 * self.pixel_size
        x1_mirror = canvas_width - x1 - self.pixel_size
        x2_mirror = x1_mirror + self.pixel_size

        # Draw the pixels
        pixel_tag = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                 fill=pixel_color, outline=pixel_color)
        mirrored_pixel_tag = self.canvas.create_rectangle(x1_mirror, y1, x2_mirror, y2,
                                                          fill=pixel_color, outline=pixel_color)

        # Create a new pixel object at the drawn location, with current size and color
        new_pixel = Pixel(x1, y1, x2, y2, self.pixel_size, pixel_color, pixel_tag)
        new_mirrored_pixel = Pixel(x1_mirror, y1, x2_mirror, y2, self.pixel_size, pixel_color, mirrored_pixel_tag)
        return new_pixel, new_mirrored_pixel
