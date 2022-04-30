import numpy as np
# from tkinter import Button

import cell


class Board:

    current_layer = 0
    game_board = None
    displayed_grid = []
    def __init__(self,dimmentions, width,height,depth = 0):
        Board.dimmentions =dimmentions
        Board.width = width
        Board.height =height
        Board.depth = depth if dimmentions == 3 else None

        Board.game_board = np.zeros((width, height), dtype=int) if dimmentions == 2 else np.zeros(( depth,width , height), dtype=int)

    def __repr__(self):
        return str(Board.game_board)

    @staticmethod
    def display_layer(location, layer):
        if Board.displayed_grid == []:

            for colloumn in  range(0,Board.height):
                colloumn_holder = []
                for row in range(0,Board.width):
                    c = cell.Cell(colloumn,row,layer[colloumn,row]==1)
                    c.create_btn_object(location)
                    c.cell_btn_object.grid(
                        column=colloumn, row=row
                    )
                    colloumn_holder.append(c)
                Board.displayed_grid.append(colloumn_holder)
        else:
            if Board.dimmentions == 2:
                for colloumn in  range(0,Board.height):
                    colloumn_holder = []
                    for row in range(0,Board.width):
                        if not( Board.displayed_grid[colloumn][row].is_active == Board.game_board[colloumn,row]):
                            Board.displayed_grid[colloumn][row].is_active = Board.game_board[colloumn, row]
                            if Board.displayed_grid[colloumn][row].is_active:
                                Board.displayed_grid[colloumn][row].cell_btn_object.configure(bg= "yellow")
                            elif not Board.displayed_grid[colloumn][row].is_active:
                                Board.displayed_grid[colloumn][row].cell_btn_object.configure(bg= "black")


            if Board.dimmentions == 3:
                for colloumn in  range(0,Board.height):
                    colloumn_holder = []
                    for row in range(0,Board.width):
                        if not( Board.displayed_grid[colloumn][row].is_active == Board.game_board[Board.current_layer,colloumn,row]):
                            Board.displayed_grid[colloumn][row].is_active = Board.game_board[Board.current_layer, colloumn, row]
                            if Board.displayed_grid[colloumn][row].is_active:
                                Board.displayed_grid[colloumn][row].cell_btn_object.configure(bg= "yellow")
                            elif not Board.displayed_grid[colloumn][row].is_active:
                                Board.displayed_grid[colloumn][row].cell_btn_object.configure(bg= "black")



        pass
    @staticmethod
    def render_layer(location, direction = "None"):

        if direction == "Next":
            Board.current_layer +=1

            Board.display_layer(location, Board.game_board[Board.current_layer])
        elif direction == "Previous":
            Board.current_layer -=1

            Board.display_layer(location, Board.game_board[Board.current_layer])

        elif direction == "None":
            if  Board.dimmentions == 3:
                Board.display_layer(location,Board.game_board[Board.current_layer])
            else:
                Board.display_layer(location, Board.game_board)
        else:


            print("an error occured during rendering of the layer")

        pass
    # useful for testing with a random board
    @staticmethod
    def random_board(precentage = 0.5):

        indices =  np.random.choice(Board.game_board.shape[1] * Board.game_board.shape[0], replace=False, size=int(Board.game_board.shape[1] * Board.game_board.shape[0] * precentage)) if Board.dimmentions == 2 else np.random.choice(Board.game_board.shape[1] * Board.game_board.shape[2] * Board.game_board.shape[0], replace=False, size=int(Board.game_board.shape[2] * Board.game_board.shape[1] * Board.game_board.shape[0] * precentage))
        Board.game_board[np.unravel_index(indices, Board.game_board.shape)] = 1

    @staticmethod
    def toggle_cell(x,y):
        if len(Board.game_board.shape) == 3:

            Board.game_board[Board.current_layer,x,y] = 0 if Board.game_board[Board.current_layer,x,y] == 1 else 1

        elif len(Board.game_board.shape) == 2:
            Board.game_board[x,y] = 0 if Board.game_board[x,y] == 1 else 1

    @staticmethod
    def set_game_board(board):
        Board.game_board = board



