#################################################################
# FILE : main.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - Paint That - Main file
#################################################################
import argparse
import tkinter as tk

from canvas import Canvas
from pixel_canvas import PixelCanvas


def main():
    """This function sets the --help flag so that the users can get instructions
    to use the Paint That, including running the program"""
    parser = argparse.ArgumentParser(description='Paint That')
    parser.add_argument('--pixel', action='store_true', help='Run "Paint That Pixel"')
    parser.add_argument('--tools', action='store_true', help='"Paint That" Tools')
    parser.add_argument('--functions', action='store_true', help='"Paint That" Functionalities')
    parser.add_argument('--about', action='store_true', help='About the project')

    args = parser.parse_args()

    # Description options
    if args.pixel:
        paint_that_pixel = tk.Tk()
        PixelCanvas(paint_that_pixel)
        paint_that_pixel.mainloop()
    elif args.tools:
        # Print explanation regarding the tools in the program
        print("\nPaint That has the following tools:\n"
              "(1) Pen:                          Free drawing.\n"
              "(2) Eraser:                       Erase parts of drawings or delete shapes.\n"
              "(3) Triangle, Rectangle, Oval:    Select and drag to position the drawings.\n"
              "(4) Polygon:                      Select points, when done - click on the first vertex.\n"
              "(5) Move:                         Click and drag any drawing to move it\n"
              "(6) Add Text:                     Add your desired text, choose font style and size.\n"
              "(6) Edit:                         Right click on any object to open a menu of options.\n")
    elif args.functions:
        # Print the different functionalities
        print("\nPaint That offers the following functionalities:\n"
              "(1) Line Width & Color Picker:    Change the line width of the drawings.\n"
              "(2) Undraw:                       Cancel the last drawing.\n"
              "(3) Redraw:                       Draw again a cancelled drawing.\n"
              "(4) Clear Canvas:                 Clear all the drawing. This operation is not undoable.\n"
              "(5) Save:                         Save your work and continue editing later.\n"
              "(6) Open:                         Load a previous work.\n"
              "(7) Export:                       Export your work as one of the supported file types.\n")
    elif args.about:
        # Print information about the project
        print('\n"Paint That" is a paint program that was made as a part of the final project in '
              'Introduction to Computer Science, made by Noam Kimhi.\n')
    else:
        # Run the program, start the event loop
        paint_that = tk.Tk()
        Canvas(paint_that)
        paint_that.mainloop()


if __name__ == "__main__":
    main()
