#################################################################
# FILE : edit_tool.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - EditTool Class
#################################################################
import tkinter as tk
from tkinter import colorchooser, simpledialog

from pen import Pen
from polygon import Polygon
from text import Text


class EditTool:
    """This is the edit tool class. can interact with shapes on a tk canvas"""

    def __init__(self, parent: tk.Canvas, drawings_list: list, prev_drawings_list: list):
        self.canvas: tk.Canvas = parent
        self.selected_shape = None
        self.prev_coords: tuple[int, int] = (0, 0)
        self.drawings_list: list = drawings_list
        self.prev_drawings_list: list = prev_drawings_list

        # Create the options in the menu - in case of pressing a shape
        self.shape_option_menu = tk.Menu(self.canvas, tearoff=0)
        self.shape_option_menu.add_command(label="Change Line Color", command=self.change_line_color)
        self.shape_option_menu.add_command(label="Change Line Width", command=self.change_line_width)
        self.shape_option_menu.add_command(label="Change Filling Color", command=self.change_filling_color)
        self.shape_option_menu.add_command(label="Move to Front", command=self.move_forward)
        self.shape_option_menu.add_command(label="Move to Back", command=self.move_backwards)
        self.shape_option_menu.add_separator()  # Separate delete option
        self.shape_option_menu.add_command(label="Delete Shape", command=self.delete_shape)

        # Create the options in the menu - in case of pressing a text
        self.text_option_menu = tk.Menu(self.canvas, tearoff=0)
        self.text_option_menu.add_command(label="Edit Text", command=self.edit_text)
        self.text_option_menu.add_command(label="Change Text Color", command=self.change_filling_color)
        self.text_option_menu.add_command(label="Change Text Size and Font", command=self.change_text_size_and_font)
        self.text_option_menu.add_command(label="Move to Front", command=self.move_forward)
        self.text_option_menu.add_command(label="Move to Back", command=self.move_backwards)
        self.text_option_menu.add_separator()  # Separate delete option
        self.text_option_menu.add_command(label="Delete Text", command=self.delete_shape)

    def start_moving(self, event):
        """This method can be bound to an even and is used to find the closest shape
        to the cursor"""
        # Get the current event x and y position
        x, y = event.x, event.y
        # Set the selected shape to the closest one to the event, and set coords
        shape_tag = self.canvas.find_closest(x, y)
        if shape_tag:
            closest_shape_index = self.drawings_list.index(shape_tag[0])
            # set the closest shape
            self.selected_shape = self.drawings_list[closest_shape_index]
        self.prev_coords = (x, y)

    def move_shape(self, event):
        """This method can be bound to an event and is used to move the selected shape"""
        # If there's a shape nearby
        if self.selected_shape:
            # Get event x and y and calculate the change in the coordinates
            x, y = event.x, event.y
            dx, dy = x - self.prev_coords[0], y - self.prev_coords[1]
            # move the selected shape according to (dx, dy) with tkinter move function
            # if shape is drawn by a pen:
            if isinstance(self.selected_shape, Pen):
                # Change the position of all ovals
                for i in range(len(self.selected_shape.oval_list)):
                    self.canvas.move(self.selected_shape.oval_list[i], dx, dy)
                    # Each single oval holds a list of [x, y, x, y] - change their position
                    single_oval_coords = self.selected_shape.oval_list_coords[i]
                    single_oval_coords[0] += dx
                    single_oval_coords[1] += dy
                    single_oval_coords[2] += dx
                    single_oval_coords[3] += dy
            elif isinstance(self.selected_shape, Polygon):
                self.canvas.move(self.selected_shape.tag, dx, dy)
                points = self.selected_shape.points
                # In polygon, points are saved in (x, y) tuples inside a list,
                # update the position of each pair
                for i in range(len(points)):
                    points[i][0] += dx
                    points[i][1] += dy
            elif isinstance(self.selected_shape, Text):
                self.canvas.move(self.selected_shape.tag, dx, dy)
                self.selected_shape.position[0] += dx
                self.selected_shape.position[1] += dy
            # else, shape is Triangle, Oval or Rectangle (behave the same)
            else:
                self.canvas.move(self.selected_shape.tag, dx, dy)
                self.selected_shape.last_x += dx
                self.selected_shape.last_y += dy
                self.selected_shape.x += dx
                self.selected_shape.y += dy
            self.prev_coords = (x, y)
            # Update the board to avoid shapes leaving a trail of color
            self.canvas.update()

    def stop_moving(self, event):
        """This method can be bound to an event, and is used when the user stopped
        moving the shape"""
        # Set the selected shape to None, and reset coordinates
        self.selected_shape = None
        self.prev_coords = None

    def on_right_click(self, event):
        """This method opens a menu of option that will be executed
        upon pressing right click"""
        x, y = event.x, event.y
        # find the index of the closest shape, if exists
        shape_tag = self.canvas.find_closest(x, y)
        if shape_tag:
            closest_shape_index = self.drawings_list.index(shape_tag[0])
            # set the closest shape
            self.selected_shape = self.drawings_list[closest_shape_index]
        # If there are shapes nearby, Display options for the user to perform
        if self.selected_shape is not None:
            if isinstance(self.selected_shape, Text):
                self.text_option_menu.post(event.x_root, event.y_root)
            else:
                self.shape_option_menu.post(event.x_root, event.y_root)

    def change_line_color(self):
        """This method changes the line color of the selected shape"""
        # ask the user for color
        _, color = colorchooser.askcolor(title="Choose Color")
        if color:
            # if received a color, set the selected shape line to color
            # If the shape is made by a pen, change both outline and fill
            if isinstance(self.selected_shape, Pen):
                # Change the color of all ovals
                self.selected_shape.color = color
                for single_oval in self.selected_shape.oval_list:
                    self.canvas.itemconfig(single_oval, fill=color, outline=color)
            # Shape is not made by pen
            else:
                self.canvas.itemconfig(self.selected_shape.tag, outline=color)
                self.selected_shape.color = color
        self.selected_shape = None

    def change_line_width(self):
        """This method changes the line width of the selected shape"""
        # ask the user for a number
        line_width = simpledialog.askinteger("Line Width", "Enter line width:")
        if line_width is not None:
            # if received an integer, set the selected shape line width to that integer
            # If the shape is made by a pen
            if isinstance(self.selected_shape, Pen):
                self.selected_shape.line_width = line_width
                # Change the color of all ovals
                for single_oval in self.selected_shape.oval_list:
                    self.canvas.itemconfig(single_oval, width=line_width)
            # Shape is not made by pen
            else:
                self.canvas.itemconfig(self.selected_shape.tag, width=line_width)
                self.selected_shape.line_width = line_width
        self.selected_shape = None

    def edit_text(self):
        """This method is used to edit the text itself"""
        new_text = simpledialog.askstring("Edit Text", "Edit your text:",
                                          initialvalue=self.selected_shape.text)
        self.selected_shape.text = new_text
        self.canvas.itemconfig(self.selected_shape.tag, text=new_text)

    def change_text_size_and_font(self):
        """This method is used to change the size and font style of the text"""
        user_input = self.selected_shape.choose_font()
        if user_input is not None:
            font_name, size = user_input
            self.selected_shape.font = (font_name, size)
            self.canvas.itemconfig(self.selected_shape.tag, font=(font_name, size))

    def change_filling_color(self):
        """This method changes the filling color of the selected shape"""
        # ask the user for color
        _, color = colorchooser.askcolor(title="Choose Color")
        if color:
            # if received a color, set the selected shape filling to color
            # If the shape is made by a pen, change both outline and fill
            if isinstance(self.selected_shape, Pen):
                self.selected_shape.color = color
                # Change the color of all ovals
                for single_oval in self.selected_shape.oval_list:
                    self.canvas.itemconfig(single_oval, fill=color, outline=color)
            # Shape is not made by pen
            elif isinstance(self.selected_shape, Text):
                self.canvas.itemconfig(self.selected_shape.tag, fill=color)
                self.selected_shape.color = color
            else:
                self.canvas.itemconfig(self.selected_shape.tag, fill=color)
                self.selected_shape.fill_color = color
        self.selected_shape = None

    def delete_shape(self):
        """This method is used to delete a shape from the board"""
        # delete the shape from the canvas
        if isinstance(self.selected_shape, Pen):
            # Delete all single ovals in the drawing
            for single_oval in self.selected_shape.oval_list:
                self.canvas.delete(single_oval)
            # Remove the drawing from drawing list
            self.drawings_list.remove(self.selected_shape)
            self.prev_drawings_list.append(self.selected_shape)
        else:
            self.canvas.delete(self.selected_shape.tag)
            # remove the shape from drawing list
            shape_to_remove = self.drawings_list.pop(self.drawings_list.index(self.selected_shape.tag))
            # add the shape to the prev drawings list
            self.prev_drawings_list.append(shape_to_remove)
        self.selected_shape = None

    def move_forward(self):
        """This method is moving the shape to the front of the board"""
        # use tkinter lift function to move the shape to the front
        # If shape is drawn by pen
        if isinstance(self.selected_shape, Pen):
            # Delete all single ovals in the drawing
            for single_oval in self.selected_shape.oval_list:
                self.canvas.lift(single_oval)
        # Shape is not drawn by pen
        else:
            self.canvas.lift(self.selected_shape.tag)
        # reorder the shape in the drawings list to save its correct position
        self.drawings_list.remove(self.selected_shape)
        self.drawings_list.append(self.selected_shape)
        self.selected_shape = None

    def move_backwards(self):
        """This method is moving the shape to the front of the board"""
        # use tkinter lift function to move the shape to the front
        # If the shape is drawn by a pen
        if isinstance(self.selected_shape, Pen):
            # Delete all single ovals in the drawing
            for single_oval in self.selected_shape.oval_list:
                self.canvas.lower(single_oval)
        # If shape is not drawn by a pen
        else:
            self.canvas.lower(self.selected_shape.tag)

        # reorder the shape in the drawings list to save its correct position
        self.drawings_list.remove(self.selected_shape)
        self.drawings_list.insert(0, self.selected_shape)
        self.selected_shape = None
