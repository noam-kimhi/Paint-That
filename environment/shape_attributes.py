#################################################################
# FILE : shape_attributes.py
# WRITER : Noam Kimhi, noam.kimhi
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - ShapeAttributes Class
#################################################################
import tkinter as tk


class ShapeAttributes:
    """This class holds two attributes in each of its objects:
    1) Color
    2) Scale Button Value
    Both attributes have getters and setters methods"""

    def __init__(self, color: str = "black", scale_var: tk.IntVar = None):
        # The value of the scale button
        self.__scale_var: tk.IntVar = scale_var
        self.__color: str = color

    def set_color(self, color: str) -> None:
        self.__color = color

    def get_color(self) -> str:
        return self.__color

    def set_line_width(self, size: int) -> None:
        self.__scale_var.set(size)

    def get_line_width(self) -> int:
        return self.__scale_var.get()
