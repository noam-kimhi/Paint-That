#################################################################
# FILE : canvas.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - Canvas Class
#################################################################
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog

import _tkinter
import canvasvg
import pygame
from PIL import ImageGrab
from reportlab.pdfgen import canvas as pdf_canvas

from edit_tool import EditTool
from eraser import Eraser
from hover_tag import HoverTag
from oval import Oval
from pen import Pen
from polygon import Polygon
from rectangle import Rectangle
from shape_attributes import ShapeAttributes
from text import Text
from triangle import Triangle


class Canvas:
    def __init__(self, root):
        # Set the given root and title of the paint program
        self.__root: tk.Tk = root
        self.__root.title("Paint That")
        self.__drawings_list: list = []
        self.__prev_drawings_list: list = []
        self.__current_shape = None

        # Set up default color (black) and line_width (5), using a variable that stores
        # the value of the scale button
        self.scale_var = tk.IntVar()
        self.scale_var.set(7)
        self.__shape_attributes = ShapeAttributes(scale_var=self.scale_var)
        # Set starting tool to pen
        self.__current_tool: str = "pen"

        # Create the canvas
        self.__canvas = tk.Canvas(root, bg="white", width=1500, height=800)
        self.__canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Add sounds
        pygame.init()
        self.bubble1_sound = pygame.mixer.Sound("bubble1.wav")
        self.bubble2_sound = pygame.mixer.Sound("bubble2.wav")
        self.bubble3_sound = pygame.mixer.Sound("bubble3.wav")
        # Lower their volume
        self.bubble1_sound.set_volume(0.05)
        self.bubble2_sound.set_volume(0.02)
        self.bubble3_sound.set_volume(0.05)

        # Play sound at init
        self.bubble2_sound.play()

        # Add buttons and update their state at the beginning of the run:

        # Hover information for the buttons
        self.hover_info = None

        # Change Line Width Button:
        label = tk.Label(root, text="Line Width")
        label.pack(side=tk.LEFT)
        self.line_width_button = ttk.Scale(root, from_=5.0, to=30.0, orient=tk.HORIZONTAL, variable=self.scale_var,
                                           command=lambda val: self.scale_var.set(val))
        self.line_width_button.pack(side=tk.LEFT, padx=5)
        self.line_width_button.bind("<Enter>", lambda event, text="(Ctrl + Mousewheel)": self.on_enter(event, text))
        self.line_width_button.bind("<Leave>", self.on_leave)

        # Change Paint Color Button:
        self.color_button = ttk.Button(root, text="Color Picker", command=self.change_color)
        self.color_button.pack(side=tk.LEFT, padx=8)
        self.color_button.bind("<Enter>", lambda event, text="Pick Shape Color\n (C)": self.on_enter(event, text))
        self.color_button.bind("<Leave>", self.on_leave)

        # A variable that stores the state according to buttons, set default to "pen" tool
        self.state = tk.StringVar(value="pen")

        # Pen button
        self.pen_button = ttk.Radiobutton(root, text="Pen", value="pen",
                                          variable=self.state, command=self.set_current_tool)
        self.pen_button.pack(side=tk.LEFT, padx=2)
        self.pen_button.bind("<Enter>", lambda event, text="Pen Tool\n (P)": self.on_enter(event, text))
        self.pen_button.bind("<Leave>", self.on_leave)

        # Eraser button
        self.eraser_button = ttk.Radiobutton(root, text="Eraser", value="eraser",
                                             variable=self.state, command=self.set_current_tool)
        self.eraser_button.pack(side=tk.LEFT, padx=2)
        self.eraser_button.bind("<Enter>", lambda event, text="Eraser Tool\n (E)": self.on_enter(event, text))
        self.eraser_button.bind("<Leave>", self.on_leave)

        # Triangle button
        self.triangle_button = ttk.Radiobutton(root, text="Triangle", value="triangle",
                                               variable=self.state, command=self.set_current_tool)
        self.triangle_button.pack(side=tk.LEFT, padx=2)
        self.triangle_button.bind("<Enter>", lambda event, text="Triangle Tool\n (T)": self.on_enter(event, text))
        self.triangle_button.bind("<Leave>", self.on_leave)

        # Rectangle button
        self.rectangle_button = ttk.Radiobutton(root, text="Rectangle", value="rectangle",
                                                variable=self.state, command=self.set_current_tool)
        self.rectangle_button.pack(side=tk.LEFT, padx=2)
        self.rectangle_button.bind("<Enter>", lambda event, text="Rectangle Tool\n (R)": self.on_enter(event, text))
        self.rectangle_button.bind("<Leave>", self.on_leave)

        # Oval button
        self.oval_button = ttk.Radiobutton(root, text="Oval", value="oval",
                                           variable=self.state, command=self.set_current_tool)
        self.oval_button.pack(side=tk.LEFT, padx=2)
        self.oval_button.bind("<Enter>", lambda event, text="Oval Tool\n (O)": self.on_enter(event, text))
        self.oval_button.bind("<Leave>", self.on_leave)

        # Polygon button
        self.polygon_button = ttk.Radiobutton(root, text="Polygon", value="polygon",
                                              variable=self.state, command=self.set_current_tool)
        self.polygon_button.pack(side=tk.LEFT, padx=2)
        self.polygon_button.bind("<Enter>", lambda event, text="Polygon Tool\n (L)": self.on_enter(event, text))
        self.polygon_button.bind("<Leave>", self.on_leave)

        # Move button
        self.move_button = ttk.Radiobutton(root, text="Move", value="edit",
                                           variable=self.state, command=self.set_current_tool)
        self.move_button.pack(side=tk.LEFT, padx=2)
        self.move_button.bind("<Enter>", lambda event, text="Move Tool\n (M)": self.on_enter(event, text))
        self.move_button.bind("<Leave>", self.on_leave)

        # Add Text button
        self.text_button = ttk.Button(root, text="Add Text", command=self.add_text)
        self.text_button.pack(side=tk.LEFT, padx=10)
        self.text_button.bind("<Enter>", lambda event, text="Add Text\n (A)": self.on_enter(event, text))
        self.text_button.bind("<Leave>", self.on_leave)

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

        # Dark Mode button
        self.bg_mode = tk.IntVar()  # A variable that stores the mode of the background
        self.dark_mode_button = ttk.Checkbutton(root, text="Dark Mode", variable=self.bg_mode,
                                                command=self.background_mode)
        self.dark_mode_button.pack(side=tk.LEFT, padx=30)

        # Mute Sounds button
        self.mute = tk.IntVar()  # A variable that stores the mode of the background
        self.mute_sound_button = ttk.Checkbutton(root, text="Mute", variable=self.mute,
                                                 command=self.mute_sound)
        self.mute_sound_button.pack(side=tk.LEFT)

        # Undraw Button
        self.undo_button = ttk.Button(root, text="Undraw", command=self.undraw)
        self.undo_button.pack(side=tk.RIGHT, padx=5)
        self.undo_button.bind("<Enter>", lambda event, text="Undraw Shape\n (Ctrl+Z)": self.on_enter(event, text))
        self.undo_button.bind("<Leave>", self.on_leave)

        # Redraw Button
        self.redo_button = ttk.Button(root, text="Redraw", command=self.redraw)
        self.redo_button.pack(side=tk.RIGHT)
        self.redo_button.bind("<Enter>", lambda event, text="Redraw Shape\n (Ctrl+Y)": self.on_enter(event, text))
        self.redo_button.bind("<Leave>", self.on_leave)

        # ALL BUTTONS ADDED #

        # Update button status:
        self.update_button_state()

        # Add Tools (only those that require it)
        self.eraser = Eraser(self.__canvas, self.__drawings_list, self.__prev_drawings_list, self.scale_var)
        self.edit_tool = EditTool(self.__canvas, self.__drawings_list, self.__prev_drawings_list)

        # Handle mouse bindings:
        # Mouse in and out of canvas:
        self.__canvas.bind("<Enter>", self.change_cursor_look)
        self.__canvas.bind("<Leave>", self.restore_cursor_look)

        # Mouse Button 1 (Left clock)
        self.__canvas.bind("<Button-1>", self.mouse_button_1_press)
        self.__canvas.bind("<B1-Motion>", self.mouse_button_1_motion)
        self.__canvas.bind("<ButtonRelease-1>", self.mouse_button_1_release)

        # Mouse Button 3 (Right click):
        self.__canvas.bind("<Button-3>", self.mouse_button_3_press)

        # Control + Mouse Wheel Up and Down
        self.__root.bind("<Control-MouseWheel>", self.control_mouse_wheel)

        # Bind Keyboard - allow user to change tool and activate buttons with keys
        self.__root.bind("<KeyPress>", self.keyboard_shortcut)
        self.__root.bind("<Control-z>", self.undraw)
        self.__root.bind("<Control-y>", self.redraw)
        self.__root.bind("<Control-s>", self.save)
        self.__root.bind("<Control-o>", self.load)
        self.__root.bind("<Control-p>", self.export)

    def on_enter(self, event: tk.Event, text: str) -> None:
        """This function defines the hover event on the tools"""
        # While presenting a tag, return
        if self.hover_info:
            return
        # Check the current event widget being hovered on and display the matching text
        if event.widget in [self.pen_button, self.eraser_button, self.triangle_button, self.rectangle_button,
                            self.oval_button, self.polygon_button, self.move_button, self.text_button,
                            self.color_button, self.line_width_button, self.clear_canvas_button, self.save_button,
                            self.load_button, self.export_button, self.undo_button, self.redo_button]:
            self.hover_info = HoverTag(event.widget, text)

    def on_leave(self, event: tk.Event) -> None:
        """This method is used to hide the hover tag"""
        if self.hover_info:
            self.hover_info.destroy()
            self.hover_info = None

    # Methods for mouse events, based on current active tool
    def mouse_button_1_press(self, event: tk.Event) -> None:
        """This method handles the left button press event"""
        if self.__current_tool == "edit":
            self.edit_tool.start_moving(event)
        if self.__current_tool == "eraser":
            self.eraser.start_erasing(event)
        # In case the shape is a polygon, it is created by multiple button 1 presses
        if isinstance(self.__current_shape, Polygon):
            self.__current_shape.choose_dots_for_polygon(event)
            if self.__current_shape.is_drawn:
                self.__drawings_list.append(self.__current_shape)
                # Add draw sfx
                self.play_sound()
                self.__current_shape = None
                return
        if self.__current_shape is None:
            if self.__current_tool == "pen":
                self.__current_shape = Pen(self.__canvas, self.__shape_attributes)
                self.__current_shape.start_drawing(event)
            elif self.__current_tool == "triangle":
                self.__current_shape = Triangle(self.__canvas, self.__shape_attributes)
                self.__current_shape.start_drawing(event)
            elif self.__current_tool == "oval":
                self.__current_shape = Oval(self.__canvas, self.__shape_attributes)
                self.__current_shape.start_drawing(event)
            elif self.__current_tool == "rectangle":
                self.__current_shape = Rectangle(self.__canvas, self.__shape_attributes)
                self.__current_shape.start_drawing(event)
            elif self.__current_tool == "polygon":
                self.__current_shape = Polygon(self.__canvas, self.__shape_attributes)
                self.__current_shape.choose_dots_for_polygon(event)

    def mouse_button_1_motion(self, event: tk.Event) -> None:
        """This method handles the left button motion event"""
        if self.__current_tool == "edit":
            self.edit_tool.move_shape(event)
        elif self.__current_tool == "eraser":
            self.eraser.erase(event)
        elif self.__current_tool == "pen":
            self.__current_shape.draw(event)
        elif self.__current_tool in ["triangle", "oval", "rectangle"]:
            self.__current_shape.draw(event)

    def mouse_button_1_release(self, event: tk.Event) -> None:
        """This method handles the left button release event"""
        if self.__current_tool == "edit":
            self.edit_tool.stop_moving(event)
        if self.__current_tool == "eraser":
            self.eraser.stop_erasing(event)
        # start the release method according to current shape, if not None
        if self.__current_shape is not None:
            if self.__current_tool == "pen":
                self.__current_shape.stop_drawing(event)
            elif self.__current_tool == "triangle":
                self.__current_shape: Triangle
                self.__current_shape.stop_drawing(event)
            elif self.__current_tool == "oval":
                self.__current_shape: Oval
                self.__current_shape.stop_drawing(event)
            elif self.__current_tool == "rectangle":
                self.__current_shape: Rectangle
                self.__current_shape.stop_drawing(event)
        # Address the case so that a single press will not create a shape
        # (polygon and pen addressed separately)
        if self.__current_tool not in ["polygon", "pen", "edit", "eraser"] and self.__current_shape.x is None:
            self.__current_shape = None
        # Address the case so that a single press in pen will not create a shape
        if self.__current_tool == "pen":
            self.__current_shape: Pen
            # A single press will not create ovals, in that case do not create a shape
            if not self.__current_shape.oval_list:
                self.__current_shape = None
        # Add the current shape to the shape list, unless its None or a polygon (explanation above)
        if self.__current_shape is not None and self.__current_tool != "polygon":
            self.__drawings_list.append(self.__current_shape)
            # Add draw sfx
            self.play_sound()
            # Reset the current shape to None
            self.__current_shape = None

    def mouse_button_3_press(self, event: tk.Event) -> None:
        """This method handles the right button press event"""
        self.edit_tool.on_right_click(event)

    def control_mouse_wheel(self, event: tk.Event) -> None:
        """Control + Scroll Up/Down event raises/lowers the value of line width.
        The values of line width range between 5 and 30"""
        # set up a delta variable. Wheel up causes positive event delta,
        # wheel down negative event delta.
        delta = 0
        if event.delta < 0 and self.scale_var.get() >= 8:
            delta = -3
        if event.delta > 0 and self.scale_var.get() <= 27:
            delta = 3
        # Change the value of scale var according to delta
        self.scale_var.set(self.scale_var.get() + delta)

    def keyboard_shortcut(self, event: tk.Event) -> None:
        """This method changes the current tool according to
        the pressed key"""
        key_actions = {
            'p': "pen",
            'e': "eraser",
            't': "triangle",
            'r': "rectangle",
            'o': "oval",
            'l': "polygon",
            'm': "edit",
            'a': self.add_text,
            'x': self.clear_canvas,
            'c': self.change_color,
        }

        # turn the pressed key into lowercase
        key_pressed = event.char.lower()
        action = key_actions.get(key_pressed)
        if action:
            if callable(action):
                action()  # If action is a function, call it
            else:
                self.state.set(action)
                self.set_current_tool()
                # Update cursor look according to new tool
                self.change_cursor_look(tk.Event())

    def play_sound(self) -> None:
        """This function plays a sound randomly out of the 3 possible sounds"""
        random.choice([self.bubble1_sound, self.bubble2_sound, self.bubble3_sound]).play()

    def set_line_width(self, str_size: str) -> None:
        """This method changes the line width, bsed on the user input"""
        # size is received as a string representing a float number
        # turn it into a float and then into an integer
        size = int(float(str_size))
        # set line width shape attributes to size
        self.__shape_attributes.set_line_width(size)
        self.eraser.eraser_size.set(size * 5)

    def change_color(self) -> None:
        """This method changes the color of the drawing, based on the user input"""
        _, color = colorchooser.askcolor(title="Choose Color")
        if color:
            # set color of shape attributes to color
            self.__shape_attributes.set_color(color)

    def clear_canvas(self) -> None:
        """This method deletes all drawings from the canvas. The user must
        first confirm that he wishes to clear the canvas."""
        user_reply = messagebox.askquestion("Clear Canvas",
                                            "Are you sure you want to clear the canvas?")
        if user_reply == "yes":
            # Delete all drawings
            self.__canvas.delete("all")
            # Clear the drawing list and the previous drawing list
            self.__drawings_list.clear()
            self.__prev_drawings_list.clear()

    def undraw(self, event: tk.Event = None) -> None:
        """This function deletes the last drawing that was made"""
        # If the drawings list is not empty
        if self.__drawings_list:
            # pop the last item in drawing list, and add it to previous drawings
            # if last drawing is made by pen
            if isinstance(self.__drawings_list[-1], Pen):
                last_drawing = self.__drawings_list.pop()
                self.__prev_drawings_list.append(last_drawing)
                # Delete all single ovals in the drawing
                for single_oval in last_drawing.oval_list:
                    self.__canvas.delete(single_oval)
            else:
                last_drawing = self.__drawings_list.pop()
                self.__prev_drawings_list.append(last_drawing)
                self.__canvas.delete(last_drawing.tag)
        return

    def redraw(self, event: tk.Event = None) -> None:
        """This function adds the last drawing that was deleted"""
        # If the previous drawings list is not empty
        if self.__prev_drawings_list:
            # pop the last item in previous drawings list, and add it to drawings
            # If last drawing is made by pen
            if isinstance(self.__prev_drawings_list[-1], Pen):
                # Remove from prev_list, add to drawings_list
                last_deleted_drawing = self.__prev_drawings_list.pop()
                self.__drawings_list.append(last_deleted_drawing)
                # Redraw
                last_deleted_drawing.draw()
                self.__canvas.update()
            else:
                last_deleted_drawing = self.__prev_drawings_list.pop()
                self.__drawings_list.append(last_deleted_drawing)
                last_deleted_drawing.draw()
                self.__canvas.update()
        return

    def add_text(self) -> None:
        """This method """
        new_text = Text(self.__canvas, self.__shape_attributes)
        new_text.draw()
        self.__drawings_list.append(new_text)

    def set_current_tool(self) -> None:
        """This method sets the current tool in use, according to the RadioButtons
        in the GUI"""
        tool = self.state.get()
        self.__current_tool = tool
        self.update_button_state()
        # Clear all polygon vertices and list of points in case
        # the user did not finish his polygon
        if isinstance(self.__current_shape, Polygon):
            self.__current_shape.delete_vertex()
            self.__current_shape.clear_points_list()
        # Reset the current state, if the tool is still polygon - create another polygon
        # Else, the current shape will be set to None.
        self.__current_shape = None

    def update_button_state(self) -> None:
        """This method disables and enables buttons according to the current state
        of the canvas' current_tool"""
        # Disable color_button when in eraser mode
        if self.__current_tool == "eraser":
            self.color_button.config(state=tk.DISABLED)
        else:
            self.color_button.config(state=tk.NORMAL)

    def background_mode(self) -> None:
        """This function changes the background color according to the
        checkbutton state"""
        if self.bg_mode.get() == 1:
            # Checkbutton is ticked, apply dark mode
            self.__canvas.config(bg="#1a1a1a")
        elif self.bg_mode.get() == 0:
            # Checkbutton is untucked, apply light mode
            self.__canvas.config(bg="white")

    def mute_sound(self) -> None:
        """This function changes the background color according to the
        checkbutton state"""
        if self.mute.get() == 1:
            # Mute is ticked, mute all sounds
            self.bubble1_sound.set_volume(0)
            self.bubble2_sound.set_volume(0)
            self.bubble3_sound.set_volume(0)
        elif self.mute.get() == 0:
            # Mute is untucked, enable all sounds
            self.bubble1_sound.set_volume(0.05)
            self.bubble2_sound.set_volume(0.02)
            self.bubble3_sound.set_volume(0.05)

    def change_cursor_look(self, event: tk.Event) -> None:
        """This method changes the cursor according to the state when on canvas"""
        cursor_dict = {
            "pen": "plus",
            "eraser": "X_cursor",
            "triangle": "plus",
            "oval": "circle",
            "rectangle": "dotbox",
            "polygon": "plus",
            "edit": "fleur"
        }

        cursor = cursor_dict.get(self.__current_tool)
        if cursor:
            self.__canvas.config(cursor=cursor)

    def restore_cursor_look(self, event: tk.Event) -> None:
        """This method is used to restore the cursor to its default appearance
        while not on the canvas"""
        self.__canvas.config(cursor="")

    @staticmethod
    def save_to_json(data: any, filename: str) -> None:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_from_json(filename: str) -> dict:
        with open(filename, 'r') as file:
            return json.load(file)

    def save(self, event: tk.Event = None) -> None:
        """This method saves the work from the canvas to a JSON file"""
        # Set a list of all the drawings in a json compatible way
        drawings_for_json = []
        for drawing in self.__drawings_list:
            # Iterate through all the drawings in drawings list
            drawings_for_json.append(drawing.save_to_dict())

        # Save drawings to JSON
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])

        # If the user entered a filename (meaning he wishes to save)
        if filename:
            self.save_to_json(drawings_for_json, filename)
            messagebox.showinfo("Project Saved", f"Data saved to {filename}")

    def load(self, event: tk.Event = None) -> None:
        """This function loads a previous work from a JSON file to the canvas"""
        # Ask the user for filename to upload from
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

        # If the user provided a filename
        if filename:
            # make sure the user provided a JSON file
            if filename.endswith('.json'):
                try:
                    drawings = self.load_from_json(filename)
                    # Clear canvas and drawings list
                    self.__canvas.delete("all")
                    self.__drawings_list.clear()
                    self.__prev_drawings_list.clear()

                    # All types of classes
                    drawing_classes = {
                        "pen": Pen,
                        "triangle": Triangle,
                        "oval": Oval,
                        "rectangle": Rectangle,
                        "polygon": Polygon,
                        "text": Text
                    }

                    # Iterate through all the dictionaries in the JSON file
                    for drawing_dict in drawings:
                        # Set the correct drawing type
                        drawing_type = drawing_dict["type"]
                        if drawing_type in drawing_classes:
                            # Set the correct object class
                            drawing_class = drawing_classes[drawing_type]
                            # Create a new drawing using the load_from_dict
                            new_drawing = drawing_class.load_from_dict(drawing_dict, self.__canvas)
                            # Draw the shape and add it to the drawing list
                            new_drawing.draw()
                            self.__drawings_list.append(new_drawing)
                except (_tkinter.TclError, KeyError, json.JSONDecodeError, TypeError):
                    # In case an exception was raised
                    messagebox.showinfo("Something's Wrong", "Some information in the file was invalid.")

    def export(self, event: tk.Event = None) -> None:
        """This function exports the painter image according to the user's chosen format"""
        filename = filedialog.asksaveasfilename(defaultextension="",
                                                filetypes=[("PDF files", "*.pdf"), ("JPEG files", "*.jpeg"),
                                                           ("SVG files", "*.svg"), ("EPS files", "*.eps")])
        # get dimensions of the canvas
        canvas_root_x = self.__canvas.winfo_rootx()
        canvas_root_y = self.__canvas.winfo_rooty()
        canvas_width = self.__canvas.winfo_width()
        canvas_height = self.__canvas.winfo_height()

        # Grab the image according to dimensions
        image = ImageGrab.grab(
            bbox=(canvas_root_x, canvas_root_y, canvas_root_x + canvas_width, canvas_root_y + canvas_height))

        if filename:
            # Save to JPEG
            if filename.endswith('.jpeg'):
                # Save the image as JPEG
                image.save(filename, "JPEG")

            # Save to PDF
            elif filename.endswith('.pdf'):
                # Paste the image onto a PDF
                pdf_image = pdf_canvas.Canvas(filename, pagesize=(canvas_width, canvas_height))
                pdf_image.drawInlineImage(image, 0, 0, width=canvas_width, height=canvas_height)
                pdf_image.save()

            # Save to SVG
            elif filename.endswith('.svg'):
                # Save to SVG using canvasvg
                with open(filename, 'w') as _:
                    canvasvg.saveall(filename, self.__canvas)

            # Save as EPS
            elif filename.endswith('.eps'):
                self.__canvas.postscript(file=filename, colormode='color')
