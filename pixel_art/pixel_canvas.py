#################################################################
# FILE : pixel_canvas.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - PixelCanvas Class
#################################################################
import _tkinter
import json
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog

import canvasvg
from PIL import ImageGrab
from reportlab.pdfgen import canvas as pdf_canvas

from hover_tag import HoverTag
from pixel import Pixel
from pixel_pen import PixelPen


class PixelCanvas:
    def __init__(self, root, pixel_size=20, grid_width=32, grid_height=32):
        self.root = root
        self.root.title("Paint That Pixel")
        self.pixel_size = pixel_size
        self.grid_width = grid_width
        self.grid_height = grid_height

        # Set canvas size to these proportions. -2 to correct edges
        self.canvas = tk.Canvas(root, width=self.grid_width * self.pixel_size - 2,
                                height=self.grid_height * self.pixel_size - 2, background="white")
        self.canvas.pack()
        self.pixel_list: list = []
        self.prev_pixel_list: list = []

        # Set up the pixel pen
        pixel_pen = PixelPen(self.canvas, pixel_size=self.pixel_size)
        self.pen: PixelPen = pixel_pen

        # Hover information for the buttons
        self.hover_info = None

        # Change Paint Color Button:
        self.left_color_button = ttk.Button(root, text="Left Color",
                                            command=lambda: self.change_color("left"))
        self.left_color_button.pack(side=tk.LEFT, padx=5)
        self.left_color_button.bind("<Enter>",
                                    lambda event, text="Pick Left Button Color\n (Q)": self.on_enter(event, text))
        self.left_color_button.bind("<Leave>", self.on_leave)

        self.right_color_button = ttk.Button(root, text="Right Color",
                                             command=lambda: self.change_color("right"))
        self.right_color_button.pack(side=tk.LEFT, padx=5)
        self.right_color_button.bind("<Enter>",
                                     lambda event, text="Pick Right Button Color\n (E)": self.on_enter(event, text))
        self.right_color_button.bind("<Leave>", self.on_leave)

        # Mirror button
        self.mirror_mode = tk.IntVar()  # A variable that stores to mode of the mirror
        self.mirror_button = ttk.Checkbutton(root, text="Mirror Mode", variable=self.mirror_mode)
        self.mirror_button.pack(side=tk.LEFT, padx=5)
        self.mirror_button.bind("<Enter>",
                                lambda event, text="Draw pixels on both\nsides of the canvas (V)": self.on_enter(event,
                                                                                                                 text))
        self.mirror_button.bind("<Leave>", self.on_leave)

        # Grid button
        self.grid_mode = tk.IntVar()  # A variable that stores to mode of the grid (show/hide)
        self.grid_button = ttk.Checkbutton(root, text="Show Grid", variable=self.grid_mode,
                                           command=self.show_grid)
        self.grid_button.pack(side=tk.LEFT, padx=5)
        self.grid_button.bind("<Enter>",
                              lambda event, text="Show / Hide Grid (G)": self.on_enter(event, text))
        self.grid_button.bind("<Leave>", self.on_leave)

        # Save
        self.save_button = ttk.Button(root, text="Save", command=self.save)
        self.save_button.pack(side=tk.RIGHT)
        self.save_button.bind("<Enter>", lambda event, text="Save Work\n (Ctrl+S)": self.on_enter(event, text))
        self.save_button.bind("<Leave>", self.on_leave)

        # Open
        self.load_button = ttk.Button(root, text="Open", command=self.load)
        self.load_button.pack(side=tk.RIGHT)
        self.load_button.bind("<Enter>",
                              lambda event, text="Load Previous Work\n (Ctrl+O)": self.on_enter(event, text))
        self.load_button.bind("<Leave>", self.on_leave)

        # Export
        self.export_button = ttk.Button(root, text="Export", command=self.export)
        self.export_button.pack(side=tk.RIGHT)
        self.export_button.bind("<Enter>",
                                lambda event, text="Export Work\n (Ctrl+P)": self.on_enter(event, text))
        self.export_button.bind("<Leave>", self.on_leave)

        # Clear Canvas
        self.clear_canvas_button = ttk.Button(root, text="Clear Canvas", command=self.clear_canvas)
        self.clear_canvas_button.pack(side=tk.RIGHT, padx=10)
        self.clear_canvas_button.bind("<Enter>", lambda event, text="Clear Canvas\n (X)": self.on_enter(event, text))
        self.clear_canvas_button.bind("<Leave>", self.on_leave)

        # Undo & Redo buttons
        self.undo_button = ttk.Button(root, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.RIGHT, padx=5)
        self.undo_button.bind("<Enter>", lambda event, text="Undo\n (Ctrl+Z)": self.on_enter(event, text))
        self.undo_button.bind("<Leave>", self.on_leave)

        self.redo_button = ttk.Button(root, text="Redo", command=self.redo)
        self.redo_button.pack(side=tk.RIGHT)
        self.redo_button.bind("<Enter>", lambda event, text="Redo\n (Ctrl+Y)": self.on_enter(event, text))
        self.redo_button.bind("<Leave>", self.on_leave)

        # Bind events to the canvas
        self.canvas.bind("<Button-1>", self.mouse_button_clicked)
        self.canvas.bind("<Button-3>", self.mouse_button_clicked)

        # Bind keys
        self.root.bind("<q>", lambda side: self.change_color("left"))
        self.root.bind("<e>", lambda side: self.change_color("right"))
        self.root.bind("<x>", self.clear_canvas)
        self.root.bind("<v>", self.change_mirror_mode)
        self.root.bind("<g>", self.change_grid_mode)
        self.root.bind("<Control-z>", self.undo)
        self.root.bind("<Control-y>", self.redo)
        self.root.bind("<Control-s>", self.save)
        self.root.bind("<Control-o>", self.load)
        self.root.bind("<Control-p>", self.export)

    def mouse_button_clicked(self, event):
        # If mirror mode is disabled
        if self.mirror_mode.get() == 0:
            # Create a new pixel, and draw it on the board
            new_pixel = self.pen.draw_pixel(event)
            # Add the new pixel to the list
            self.pixel_list.append(new_pixel)
        else:
            # Create 2 new pixel, original and mirrored
            new_pixel, mirrored_pixel = self.pen.draw_pixel_mirror(event)
            # Add the pixels to the list, in case they are not white (bg color)
            self.pixel_list.append(new_pixel)
            self.pixel_list.append(mirrored_pixel)
        # If the grid was activated, reapply it
        if self.grid_mode.get() == 1:
            self.draw_grid()

    def change_color(self, side) -> None:
        """This method changes the color of the drawing,
        based on the user input"""
        _, color = colorchooser.askcolor(title=f"Choose {side} color")
        if color:
            # If the user gave a color, the given side color
            # will change to the desired color
            self.pen.set_color(color, side)
            return

    def on_enter(self, event: tk.Event, text: str) -> None:
        """This function defines the hover event on the tools"""
        # While presenting a tag, return
        if self.hover_info:
            return
        # Check the current event widget being hovered on and display the matching text
        if event.widget in [self.right_color_button, self.left_color_button, self.clear_canvas_button, self.save_button,
                            self.export_button, self.load_button, self.redo_button, self.undo_button,
                            self.mirror_button, self.grid_button]:
            self.hover_info = HoverTag(event.widget, text)

    def on_leave(self, event: tk.Event) -> None:
        """This method is used to hide the hover tag"""
        if self.hover_info:
            self.hover_info.destroy()
            self.hover_info = None

    def draw_grid(self) -> None:
        """This method draws lines in a grid on the canvas, in jumps the size of a pixel"""
        for i in range(0, self.grid_width * self.pixel_size, self.pixel_size):
            self.canvas.create_line([(i, 0), (i, self.grid_height * self.pixel_size)], fill="#d3d3d3", tags="grid")
        for i in range(0, self.grid_height * self.pixel_size, self.pixel_size):
            self.canvas.create_line([(0, i), (self.grid_width * self.pixel_size, i)], fill="#d3d3d3", tags="grid")

    def show_grid(self) -> None:
        """This method shows and hides the grid based on grid_mode value (checkbutton)"""
        if self.grid_mode.get() == 1:
            # Grid button is ticked, show all grid lines
            self.draw_grid()
        else:
            # Grid button is untucked, delete all grid lines
            self.canvas.delete("grid")

    def change_mirror_mode(self, event: tk.Event) -> None:
        """This method changes the mirror mode with keys"""
        if self.mirror_mode.get() == 0:
            self.mirror_mode.set(1)
        else:
            self.mirror_mode.set(0)

    def change_grid_mode(self, event: tk.Event) -> None:
        """This method changes the grid mode with keys"""
        if self.grid_mode.get() == 0:
            self.grid_mode.set(1)
            self.draw_grid()
        else:
            self.grid_mode.set(0)
            self.canvas.delete("grid")

    def undo(self, event: tk.Event = None) -> None:
        # If the pixel list is not empty
        if self.pixel_list:
            last_pixel = self.pixel_list.pop()
            self.prev_pixel_list.append(last_pixel)
            self.canvas.delete(last_pixel.tag)
        return

    def redo(self, event: tk.Event = None) -> None:
        # If the pixel list is not empty
        if self.prev_pixel_list:
            last_deleted_pixel = self.prev_pixel_list.pop()
            self.pixel_list.append(last_deleted_pixel)
            self.pen.draw_pixel(None, last_deleted_pixel)
        return

    def clear_canvas(self, event: tk.Event = None) -> None:
        """This method deletes all pixels from the canvas. The user must
        first confirm that he wishes to clear the canvas."""
        user_reply = messagebox.askquestion("Clear Canvas",
                                            "Are you sure you want to clear the canvas?")
        if user_reply == "yes":
            # Delete all drawings
            self.canvas.delete("all")
            # Clear the drawing list and the previous drawing list
            self.pixel_list.clear()
            self.prev_pixel_list.clear()
            # Clearing canvas deletes the grid, apply it again
            if self.grid_mode.get() == 1:
                self.draw_grid()

    @staticmethod
    def save_to_json(data: any, filename: str) -> None:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_from_json(filename: str) -> dict:
        with open(filename, 'r') as file:
            return json.load(file)

    def save(self, event: tk.Event = None) -> None:
        # Set a list of all the drawings in a json compatible way
        pixels_for_json = []
        for drawing in self.pixel_list:
            # Iterate through all the drawings in drawings list
            pixels_for_json.append(drawing.save_to_dict())

        # Save drawings to JSON
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        # If the user entered a filename (meaning he wishes to save)
        if filename:
            self.save_to_json(pixels_for_json, filename)
            messagebox.showinfo("Project Saved", f"Data saved to {filename}")

    def load(self, event: tk.Event = None) -> None:
        # Ask the user for filename to upload from
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

        # If the user provided a filename
        if filename:
            # make sure the user provided a JSON file
            if filename.endswith('.json'):
                try:
                    drawings = self.load_from_json(filename)
                    # Clear canvas and drawings list
                    self.canvas.delete("all")
                    self.pixel_list.clear()
                    self.prev_pixel_list.clear()

                    # Iterate through all the pixel dictionaries in the JSON file
                    for pixel_dict in drawings:
                        new_pixel = Pixel.load_from_dict(pixel_dict)
                        # Draw the shape and add it to the drawing list
                        self.pen.draw_pixel(None, new_pixel)
                        self.pixel_list.append(new_pixel)
                except (_tkinter.TclError, KeyError, json.JSONDecodeError, TypeError):
                    # In case an exception was raised
                    messagebox.showinfo("Something's Wrong", "Some information in the file was invalid.")

    def export(self, event: tk.Event = None) -> None:
        # Before exporting, delete grid
        self.canvas.delete("grid")

        filename = filedialog.asksaveasfilename(defaultextension="",
                                                filetypes=[("PDF files", "*.pdf"), ("JPEG files", "*.jpeg"),
                                                           ("SVG files", "*.svg"), ("EPS files", "*.eps")])
        # get dimensions of the canvas
        canvas_root_x = self.canvas.winfo_rootx()
        canvas_root_y = self.canvas.winfo_rooty()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Grab the image according to dimensions
        image = ImageGrab.grab(
            bbox=(canvas_root_x, canvas_root_y, canvas_root_x + canvas_width, canvas_root_y + canvas_height))

        if self.grid_mode.get() == 1:
            # If the grid was shown, reapply it
            self.draw_grid()

        if filename:
            # Save to JPEG
            if filename.endswith('.jpeg'):
                # Save the image as JPEG
                image.save(filename, "JPEG")

            # Save to PDF
            elif filename.endswith('.pdf'):
                # Paste the image onto a PDF
                c = pdf_canvas.Canvas(filename, pagesize=(canvas_width, canvas_height))
                c.drawInlineImage(image, 0, 0, width=canvas_width, height=canvas_height)
                c.save()

            # Save to SVG
            elif filename.endswith('.svg'):
                # Save to SVG using canvasvg
                with open(filename, 'w') as _:
                    canvasvg.saveall(filename, self.canvas)

            # Save as EPS
            elif filename.endswith('.eps'):
                self.canvas.postscript(file=filename, colormode='color')
