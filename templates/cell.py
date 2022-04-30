import Board
from tkinter import Button, PhotoImage
import tkinter.font as tkFont


class Cell:
    """
    class for the button's as living cells in the game of life
    """

    def __init__(self,x,y,activated = False):
        # x and y variables refer to the location of the button and activated = True means the cell is alive

        self.is_active = activated
        self.x = x
        self.y = y
        self.cell_btn_object = None
    def create_btn_object(self, location):

        # makes the button which the cell is conected to, black is dead yellow is allive
        btn = Button(
            location,
            bg="black" if self.is_active == False else "yellow",

        )

        # adds the onclick toggle event
        btn.bind('<Button-1>', self.update_cell ) # Left Click
        self.cell_btn_object = btn
        return self

    def update_cell(self,event):
        # on update change the background colour and is_active variables dependent
        # on the original state

        if self.is_active:
            self.cell_btn_object.configure(bg= "black")
            self.is_active = False
        else:
            self.cell_btn_object.configure(bg= "yellow")
            self.is_active = True

        # toggle the sell in the board itself
        Board.Board.toggle_cell(self.x,self.y)
