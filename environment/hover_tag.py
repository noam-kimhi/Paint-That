#################################################################
# FILE : hover_tag.py
# WRITER : Noam Kimhi, noam.kimhi
# EXERCISE : intro2cs Final Project
# DESCRIPTION: Paint Program - HoverTag Class
#################################################################
import tkinter as tk


class HoverTag(tk.Toplevel):
    def __init__(self, canvas: tk.Canvas, text: str):
        tk.Toplevel.__init__(self, canvas)
        self.overrideredirect(True)
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty() - 30  # Adjust the y-coordinate to position above the button
        self.geometry("+{}+{}".format(x, y))
        self.label = tk.Label(self, text=text, bg='white', borderwidth=1, relief='solid')
        self.label.pack(ipadx=1)
