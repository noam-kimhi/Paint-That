#################################################################
# FILE : polygon.py
# WRITER : Noam Kimhi, noam.kimhi, ID: 322678947
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - Polygon Class
#################################################################
import tkinter as tk
import typing

from shape_attributes import ShapeAttributes


class Polygon:
    """This is the Polygon Tool in the Paint program. Has attributes:
            1. Canvas - The space on which the cursor input is received from, and
            the area on which the polygon is painted.
            2. Color of the polygon
            3. Line width of the polygon
            """

    def __init__(self, canvas: tk.Canvas, shape_attributes: ShapeAttributes, tag: typing.Optional[int] = None,
                 points: typing.Optional[list[list]] = None,
                 color: typing.Optional[str] = None,
                 line_width: typing.Optional[int] = None,
                 fill_color: str = ""):

        # Set the main attributes of the polygon
        self.canvas = canvas
        self.shape_attributes = shape_attributes
        self.color = color
        self.line_width = line_width
        self.fill_color = fill_color
        # Set up a boolean for when the shape is done
        self.is_drawn: bool = False
        self.tag = tag

        # A list of points that will determine the coordinates for the polygon.
        # If given points, create with points from parameter.
        self.points = points or []

    def __eq__(self, other: int) -> bool:
        """This method is used to determine if the tag of self is equal to another tag"""
        return self.tag == other

    def choose_dots_for_polygon(self, event) -> None:
        """This method will be bound to an event, and add index (x,y) to points
        list, until adding a point that is approximately close to the first vertex in the group,
        meaning all vertices are drawn"""
        # Get the new coordinates from the event
        x, y = event.x, event.y
        # A polygon must have at least 3 vertices
        if len(self.points) >= 3:
            # Get the (x, y) of the first vertex
            x_coord, y_coord = self.points[0]
            # If the current vertex is approximately close to the original, draw the polygon
            # delete all guiding vertices and clear points list
            if (x_coord - 15 <= x <= x_coord + 15) and (y_coord - 15 <= y <= y_coord + 15):
                self.color = self.shape_attributes.get_color()
                self.line_width = self.shape_attributes.get_line_width()
                self.draw()
                self.is_drawn = True
                # self.clear_points_list()  # Reset points for the next polygon
                self.delete_vertex()  # Delete all guiding vertices
            # If it is not adjacent, add to the list and draw guiding vertex
            else:
                self.points.append([x, y])
                self.draw_vertex(x, y)
        else:
            # If there are less than 3 points, do not try to draw polygon,
            # instead draw a guiding vertex and add to the list.
            self.points.append([x, y])
            if len(self.points) == 1:
                # If this is the first vertex, place the special one
                self.draw_first_vertex(x, y)
            else:
                # If not, create a normal vertex
                self.draw_vertex(x, y)

    def draw(self) -> None:
        """This function draws the polygon based on the list of points"""
        self.tag = self.canvas.create_polygon(self.points, fill=self.fill_color,
                                              outline=self.color,
                                              width=self.line_width)

    def draw_first_vertex(self, x: int, y: int) -> None:
        """This method is used to create the first vertex, that will appear differently
        than the rest to indicate the starting point"""
        self.canvas.create_oval(x + 1, y + 1, x - 1, y - 1, fill="",
                                outline="#ad153b",
                                width=self.shape_attributes.get_line_width(), tags="vertex")

    def draw_vertex(self, x: int, y: int) -> None:
        """This method is used to create guiding vertices that will be
        deleted later upon completing the polygon"""
        self.canvas.create_oval(x + 1, y + 1, x - 1, y - 1, fill="",
                                outline=self.shape_attributes.get_color(),
                                width=self.shape_attributes.get_line_width(), tags="vertex")

    def delete_vertex(self) -> None:
        """This method is used to delete all vertex"""
        self.canvas.delete("vertex")

    def clear_points_list(self) -> None:
        """This method is used to empty the points list"""
        self.points = []

    def save_to_dict(self) -> dict:
        """This method saves the data of a drawn polygon to the dictionary"""
        # Save the data of the polygon to the dictionary
        polygon_dict = {"type": "polygon",
                        "data": {"shape_attributes": {"color": self.shape_attributes.get_color(),
                                                      "scale_var": self.shape_attributes.get_line_width()},
                                 "tag": self.tag,
                                 "points": self.points,
                                 "color": self.color,
                                 "fill_color": self.fill_color,
                                 "line_width": self.line_width}
                        }
        return polygon_dict

    @classmethod
    def load_from_dict(cls, polygon_dict: dict, canvas: tk.Canvas) -> object:
        # Get the info from polygon_dict

        # Create a shape attribute object
        raw_shape_attributes = polygon_dict["data"].pop("shape_attributes")
        scale_var = tk.IntVar()
        scale_var.set(raw_shape_attributes["scale_var"])
        shape_attributes = ShapeAttributes(color=raw_shape_attributes["color"],
                                           scale_var=scale_var)

        # Create a new polygon
        new_polygon = cls(canvas=canvas, shape_attributes=shape_attributes, **polygon_dict["data"])
        return new_polygon
