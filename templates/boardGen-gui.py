from tkinter import *

import numpy

from Board import Board
import matplotlib.pyplot as plt
from matplotlib import colors
from tkinter.messagebox import showinfo
import numpy as np
import argparse
import os



# the GUI is set at a fixed width, change it here but note the button area doesnt get bigger
window_size_width = 450
window_size_height = 300

# sets command line arguments and adds them to the args variable
parser = argparse.ArgumentParser(description='sets board for the base case of conways game of life ')
parser.add_argument('--filename', type=str,default="./",help =  "the file/folder to form the basis of the board, for more information on files see readme\n None = use random, give i directory ending in \"/\" for 3d use \"./\" for the local folder ") ## default added here for testing
parser.add_argument('--width', type=int, default = 15,metavar="[0-100]", choices=range(1,100),help = "sets the width of the board for board generation, WARNING WHILE SETTING HIGHER WILL GIVE YOU A LARGER BOARD IT WILL TAKE LONGER TO OPEN THE FILE FOR THE FIRST TIME (defualt = 15)")
parser.add_argument('--height', type=int, default = 15,metavar="[0-100]", choices=range(1,100),help =  "sets the height of the board for board generation, WARNING WHILE SETTING HIGHER WILL GIVE YOU A LARGER BOARD IT WILL TAKE LONGER TO OPEN THE FILE FOR THE FIRST TIME (defualt = 15)")
parser.add_argument('--dimensions', type=int, default = 2, choices=[2,3],help = "set to 2 if the conway save will be 2D or 3D (defualt = 2)")
parser.add_argument('--depth', type=int, default = 10,metavar="[0-250]", choices=range(1,250),help = "How many layers deep (3D only) do you want the board. setting this higher doesn't effect the GUI opening time as much as heightxwidth")
parser.add_argument('--random', type=float, default = 0.2,metavar="[0.00-1.00]",help = "set any float between 0 and 1 to be the percentage of alive cells given to an original board. 0 = dead board - 1 = 100 percent living board. Can be reset within the UI (default = 0.0)")

args = parser.parse_args()


# creates a new Board object as board
board = Board(args.dimensions,args.width,args.height,args.depth)


# some variables required for displaying a 2d image without the pixels mixing colours if all alive
# set colours bellow for left = dead, right = alive
cmap = colors.ListedColormap(['black','yellow'])


def save_board(event=None):
    """
    function for save button, for all layers in the board save them as a file
    """


    # function to save 2D board
    if len(board.game_board.shape) == 2:
        # if the filename is set to its default then give the filename output else take the file name from the command line
        if args.filename == "./":
            filename = "output"
        else:
            filename = args.filename

        # open the file
        file = open(str(filename)+".txt","w")

        # take the x,y coordinates from the game board where the living cells are then itterate over them
        index = np.where(numpy.flip(board.game_board,0) == 1)
        # index = np.where(board.game_board == 1)

        for x in range (0,len(index[0])):
            # write to the file the x,y values from the index with new line charecter so it can be read later
            file.write(str(index[0][x])+","+str(index[1][x])+"\n")


    # function to save 3D board

    elif len(board.game_board.shape) == 3:
        # take the layer number as depth and the x,y board as a 2d slice of the 3d board in position depth as layer
        for depth, layer in enumerate(board.game_board):

            # oepn a new file in the folder provided as the command line as the current layer number .txt
            file = open(args.filename + str(depth)+".txt","w")

            ## save in the same way as above
            index = np.where(layer == 1)
            for x in range(0, len(index[0])):
                file.write(str(index[0][x]) + "," + str(index[1][x]) + "\n")



    # test to find if the board is set correctly since a board with 4 layers shouldn't go ahead
    else:
        showinfo("Window", "an error has occured when trying to save the board")

    #popup window confirming completion
    showinfo("Window", "save complete")


def previous_slice(event=None):
    """
    function for previous layer button for 3D boards
    """

    # decrement the board current layer
    board.current_layer -=1

    # if the board is still within the bounds of the number of layers of the board then render the new layer

    if board.current_layer >= 0 and board.current_layer < args.depth:
        board.render_layer(main_frame,"Previous")

    # if the boards new current layer is less than 0 incriment the value back to 0 then pop up an error window
    elif board.current_layer < 0:
        board.current_layer += 1

        showinfo("Window", "this slice doesn't exist (no layers exist below slice 0)")


    #updates layercounter

    layer_counter.configure( text= f"Currently veiwing layer {board.current_layer}")

def next_slice(event=None):
    """
    function for next layer button for 3D boards
    """
    # increment  the board current layer

    board.current_layer +=1

    # if the board is still within the bounds of the number of layers of the board then render the new layer

    if board.current_layer >= 0 and board.current_layer < args.depth:
        board.render_layer(main_frame,"Next")
    # if the boards new current layer is greater than the number of layers in the board
    # decrement the value back to the original layer number then pop up an error window

    elif board.current_layer >= args.depth:
        board.current_layer -= 1

        showinfo("Window", "this slice doesn't exist (the slice is greater then the requested maximum)")

    #updates layercounter
    layer_counter.configure( text= f"Currently veiwing layer {board.current_layer}")



def load_board(board):
    board_copy = np.zeros(Board.game_board.shape, dtype=int)
    if len(Board.game_board.shape)== 3:

        list_of_files = [x for x in os.listdir(args.filename) if
                         x.endswith(".txt") and x[:-4].isnumeric() and int(x[:-4]) >= 0]




        for filename in list_of_files:
            file = open(args.filename + filename, "r")
            for line in file.readlines():
                coordinate = line[:-1].split(",")
                board_copy[int(filename[:-4]),int(coordinate[0]),int(coordinate[1])] = 1
        Board.set_game_board(board_copy)
        board.render_layer(main_frame)
    elif len(Board.game_board.shape) == 2:
        if len(board.game_board.shape) == 2:
            if args.filename == "./":
                filename = "output"
            else:
                filename = args.filename
        try:
            file = open(filename + ".txt", "r")
        except:
            showinfo("error", "the file you entered doesn't exist")
            return

        for line in file.readlines():
            coordinate = line[:-1].split(",")
            board_copy[int(coordinate[0]),int(coordinate[1])] = 1
        Board.set_game_board(board_copy)
        board.render_layer(main_frame)
    else:
        showinfo("error", "error loading data")

    showinfo("Window", "load complete")

def new_board():
    """
    function for new board button for 3D and 2d boards
    this function sets any board to being empty/dead
    """

    # run the set board function on a numpy array of all zeros which is the same dimensions as given in the command line
    Board.set_game_board(np.zeros(board.game_board.shape, dtype= int))

    #display the board in the window
    board.render_layer(main_frame)

    # pop up confirmation
    showinfo("Window", "blank board generated")

def random_board_creation (percentage =  None):
    """
    function for new board generate button for 3D and 2d boards found in the random poput window
    this function sets any board to having the number of living pixels = board_width * board_height * board_depth * percentage_of_living_cells
    if percentage = 1 the whole board is living
    if percentage = 0 the whole board is dead
    if percentage = 0.5 half of all cells are living
    """

    # run the set board function on a numpy array of all zeros which is the same dimensions as given in the command line

    Board.set_game_board(np.zeros(board.game_board.shape, dtype= int))

    # the percentage is given as a string due to tkinter limitations. check if the string exists, has only 1 "." and is
    # only made of numbers. then ensure the value of the float is between 0 and 1
    if percentage and percentage.replace('.','',1).isdigit() and float(percentage) >= 0.0 and float(percentage) <= 1.0:
        # if the percentage passes validation set a new boad with the random_board method with the new percentage
        validated_percentage = float(percentage)
        board.random_board(validated_percentage)

        # render the layer then show a completion pop up
        board.render_layer(main_frame)
        showinfo("Window", "random board generated")
        # close the pop up window where the user entered the percentage
        pop_up_random.destroy()

    else:
        showinfo("error",
                 "pleese enter a floating point number between 0 and 1")


def random_board_instruction():
    """
    simple instructions pop up for the random board popup window, if the button (i) for information is pressed.
    """
    showinfo("information", "please enter a number between 0.0 and 1.0. \nthe closer the number is to 0 the less the board will be filled\nwhile the closer the number is to 1 the more of the board will be filled.\ni.e. 1 means all squares are considered alive")

def random_board():

    # make a new pop up window and set basic perameters. (title, name, which tkinter winow to bind it too)
    # window is set as global so it can be closed elsewhere
    global pop_up_random

    pop_up_random = Toplevel(root)
    pop_up_random.title("New Random Board")
    pop_up_random.geometry("300x300")

    # within the pop up window add a frame to fill the popup

    pop_up_frame = Frame(pop_up_random)
    pop_up_frame.place(x=0,y=0)

    # add some information and extra buttons including an entry window for the user to enter the percentage of living cells
    global random_variable
    random_variable = Entry (pop_up_frame, text= "enter a value between 0.0 and 1.0")
    random_variable.grid(column=1, row = 1)

    # add a button for generating the grid

    procede_button = Button (pop_up_frame, text = "generate",command= lambda : random_board_creation (random_variable.get()))
    procede_button.grid(column=1, row = 5)

    # add a button for instructions
    information = Button (pop_up_frame, text = "(i)",command= random_board_instruction)
    information.grid(column=1, row = 3)

def display():
    # if the board is 3D
    if len(board.game_board.shape) == 3:

        # figure size and other variables required for matplotlib to display a 3d graph
        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # sets original elevation and azimuth of the camera for the 3d plot (can be changed by click and drag in the plt window)
        ax.view_init(65,65)

        # takes a list of indecies where there is a living cell from the x axis and store the index of living cells into x,
        # from the z axis and store the index of living cells into z, etc.
        z, x, y = board.game_board.nonzero()

        # display the 3d scatter plot
        ax.scatter(x, y, z, c=z, alpha=1, s=10, marker="s", edgecolors="black")
        plt.show()


    # if the board is 2D

    elif len(board.game_board.shape)== 2:
        #consider the board as a colour map with each index refering to a living cell colour 1 and deadcells coloured 0
        # boardness = numpy.flip(board.game_board,0)
        plt.imshow( numpy.flip(board.game_board,0), interpolation='nearest', origin='lower',
                         cmap=cmap, vmin=0, vmax=1)

        plt.show()
    else:
        showinfo("information",
                 "error in board display")


if __name__ == "__main__":


    # make a new tkinter window as root and set the name, size of the window and disable resizing of the window
    root = Tk()
    root.geometry(f'{window_size_width}x{window_size_height}')
    root.title("Conways Game of life Board Generator")
    root.resizable(False, False)

    # add a menu bar to the top of the root
    menubar = Menu(root)


    filemenu = Menu(menubar, tearoff=0)
    # adds functions to the menu bar including the file dropdown section

    filemenu.add_command(label="New", command=new_board)
    filemenu.add_command(label="load", command=lambda: load_board(board))
    filemenu.add_command(label="Save", command=save_board)
    filemenu.add_command(label="random", command=random_board)

    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_command(label="display as plot", command=display)

    if args.dimensions == 3:
        menubar.add_command(label="previous layer", command=previous_slice)
        menubar.add_command(label="next layer", command=next_slice)
        # adds a label to the bottom menu bar to display the current layer number, updated when moving through layers

        layer_counter = Label(root, text="Currently veiwing layer 0")

        layer_counter.pack(side=BOTTOM, fill=X)

    root.config(menu=menubar)




    ## the following is based on a tutorial given by codemy.com in the generation of scroll bars with tkinter
    # Create A Canvas
    canvas_window = Canvas(root)
    canvas_window.pack(side=LEFT, fill=BOTH)

    # Add A Scrollbar To The Canvas for the y axis
    my_scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas_window.yview)
    my_scrollbar.pack(side=LEFT, fill=Y)
    # Add A Scrollbar To The Canvas for the y axis
    scrollbar = Scrollbar(root, orient=HORIZONTAL, command=canvas_window.xview)
    scrollbar.pack(side=TOP, fill=X)

    # Configure The Canvas
    canvas_window.configure(yscrollcommand=my_scrollbar.set)
    canvas_window.bind('<Configure>', lambda e: canvas_window.configure(scrollregion=canvas_window.bbox("all")))




    canvas_window.configure(xscrollcommand=scrollbar.set)
    canvas_window.bind('<Configure>', lambda e: canvas_window.configure(scrollregion=canvas_window.bbox("all")))

    # adds a frame to the canvas for adding the buttons too
    main_frame = Frame(canvas_window)

    # add the button frame to the canvas
    canvas_window.create_window((0, 0), window=main_frame, anchor="nw")

    # generate the random board then display it
    board.random_board(args.random)
    board.render_layer(main_frame)



    # Run the window
    root.mainloop()
