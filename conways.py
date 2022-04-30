


from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import argparse
import imageio
from matplotlib import colors
import os

import matplotlib.pyplot as plt

# sets numpy seed for reproducibility


# REMOVE THIS FOR RANDOM BOARDS
#np.random.seed(19680801)

# adds the many command line arguments, see readme for full description and tutorial

parser = argparse.ArgumentParser(description='sets up conways game of life ')
parser.add_argument('--filename', type=str,default=None, help = "the file/folder to form the basis of the board, for more information on files see readme\n None = use random, give i directory ending in \"/\" for 3d") ## default added here for testing templates/
parser.add_argument('--gif', type=str, default = "output.gif" , help = "the output of the function wll be saved as a gif, give the NAME.gif or a path to the output here (default output.gif)")
parser.add_argument('--scale', type=int, default =1 , choices=range(1,25),metavar="[0-25]" , help = "2D only - if unchanged each cell will be one pixel, scales the gif by a whole number of pixels so zoom the image in, the greater the scale the longer the iterations (default = 1)")

parser.add_argument('--iterations', type=int, default = 100, help = "number of times a board is updated using the game of life rules. (default 100)")
parser.add_argument('--width', type=int, default = 15, choices=range(1,250),metavar="[0-250]",help = "Number of cells wide the board will be when its being run, suggested to have a square board width = height (defualt = 15)")
parser.add_argument('--height', type=int, default = 15, choices=range(1,250),metavar="[0-250]",help = "Number of cells tall the board will be when its being run, suggested to have a square board width = height (defualt = 15)")
parser.add_argument('--dimensions', type=int, default = 2, choices=[2,3],help = "set to 2 if the conway save will be 2D or 3D (defualt = 2)")
parser.add_argument('--depth', type=int, default = 15, choices=range(1,250),metavar="[0-250]",help = "Number of cells deap (in the third dimention) the board will be when its being run, suggested to have a square board width = height (defualt = 15)")
parser.add_argument('--random', type=float, default = 0.2,metavar="[0.00-1.00]",help = "set any float between 0 and 1 to be the percentage of alive cells given at random on a board. only used if filename is not set")
parser.add_argument('--wrap', action='store_true', help = "In 2d wrap the board around so it forms a sphere of points not a flat field. (default True)")


# parser.add_argument('--reproduction', type=int, default = 3, help="the number of living neighbours required for reproduction, i.e before a cell is alive")
parser.add_argument('--min_living', type=int, default = 2, help="minumum number of living cells required before underpopulation removes the cell")
parser.add_argument('--max_living', type=int, default = 3, help="maximum number of living cells required before overpopulation removes the cell")

parser.add_argument('--min_reproduction', type=int, default = 3, help="the number of living neighbours required for reproduction, i.e before a cell is alive (used for 3d)")
parser.add_argument('--max_reproduction', type=int, default = 3, help="the number of living neighbours required for reproduction, i.e before a cell is alive (used for 3d)")
parser.add_argument('--elevation', type=int, default = 75, help="when saving a 3D plot, as an angle directed at the origin. At what elevation would you like the cammera (default 75)")
parser.add_argument('--azimuth_incriment', type=float, default = 1.2, help="the angle of spin per frame of the 3d gif, set to 0 for stationary camera, set higher for quicker orbit. higher orbits look choppier.(default 1.2)")
parser.add_argument('--fps', type=int, default = 5, help="Frames per second for the animation, lower gives more detail at each stage but longer animation (default 5)")

parser.add_argument('--gridlines', action='store_true',help="If set in the command line will remove the 3d border and edges from output gif")
parser.add_argument('--completion', action='store_true', help = "WARNING USE IF YOU KNOW THE INPUT TERMINATES. if set true the board will be run through conways until two consecutive outputs are the same.")
parser.add_argument('--everyx', type=int, default = None, choices=range(-1,9999999),metavar="",help = "how often to display the board on screen before saving it as a gif, if left unset then no boards will be displayed, if set to 5 every 5 boards will be displayed (defualt = None) \n - set to -1 to not display")



args = parser.parse_args()



def cells_template_reader(board, file):
    """
    takes a 2D numpy array game board and cells file and returns the board with living cells = 1 following the .cells format

    :param board: a N x N numpy nandaray refuring to a conway board for the game of life
    :param file: the file path to a .cells file
    :return: the updated board after it has been taken the data from the cells file
    """

    read = open(file, "r")

    for index, line in enumerate( read.readlines()):
        # if the value at the start of the line does not mark a comment
        if line[0] != "!":
            # itterate through the list of living cells taken by finding the O from the .cells file
            for found_index in [i for i in range(len(line)) if line.startswith('O', i)]:
                # try to add the living cell to the indecies on the board, exeption will be raised if the cell is out of range for the board
                try:
                    board[index][found_index] = 1
                except:
                    pass


    # return the updated board
    return board




def add_living_file_2d(board,file):
    """

    :param board: a N x N numpy nandaray refuring to a conway board for the game of life
    :param file: the file path to a .cells file or a .txt file where each line is an X,Y coordinate refering to a living cell
    :return: updated game board
    """


    # if the file is in cells format use the cells function
    if file[-6:] == ".cells":
        board = cells_template_reader(board,file)

        return board
    # else assume the file is in .txt format
    else:
        read = open(file+".txt","r")

        # each line should be an x,y coordinate, go from the line as a string to a coordinate and set the position to 1
        for line in read.readlines():
            try:
                coordinate = line[:-1].split(",")
                board[int(coordinate[0]), int(coordinate[1])] = 1
            except:
                pass

    # return the updated board
    return board


def add_living_file_3d(board,file):
    """

    :param board: a N x N x M numpy nandaray refuring to a conway board for the game of life
    :param file: the filepath to a folder with files named 0.xxx 1.xxx n.xxx where n referes to the layer the file will be added to
    the files within the folder should be either - a .cells file or a .txt file where each line is an X,Y coordinate refering to a living cell
    :return: updated game board
    """

    # takes all files in the folder with either a .cells or .txt type
    list_of_files = [x for x in os.listdir(file) if
                     x.endswith(".txt") and x[:-4].isnumeric() and int(x[:-4]) >= 0]
    list_of_files.extend( [x for x in os.listdir(file) if
                     x.endswith(".cells")  and x[:-6].isnumeric() and
                                 int(x[:-6]) >= 0])
    # itterate over the found files
    for filename in list_of_files:
        # if cells file send a 2D slice of the 3D board to the cells template reader
        if filename.endswith(".cells"):

            board[int(filename[:-6])] = cells_template_reader(board=board[int(filename[:-6])], file = file+ filename)
        else:
            # if the file is a txt file itterate like for a 2d file
            filet = open(file+ filename, "r")

            for line in filet.readlines():
                try:

                    coordinate = line[:-1].split(",")
                    board[int(filename[:-4]),int(coordinate[0]),int(coordinate[1])] = 1

                except:
                    pass

    return board

def update_3d(board,width,height,depth):
    """

    :param board: 3d numpy nandarray board with 1 = living cell and 0 = a dead cell
    :param width: :param height: the NXN of a single layer in the game board
    :param depth: the number of layers in the game board
    :return: an updated 3d numpy ndarray after putting the original over the rules of the 3d game
    """
    # take a copy of the board at the origin point so all calculations can be taken at
    # the point of the board update being initiated

    coppied_board = board.copy()
    # itterate over all items in the items in the board

    for aisle in range (board.shape[0]):
        for colloumn in range (0,board.shape[1]):
            for row in range (0,board.shape[2]):

                living_neighbours = np.sum(board[aisle-1 if aisle-1 > 0 else 0:aisle+2 if aisle+2 <= board.shape[0] else board.shape[0],
                       colloumn-1 if colloumn-1 >=0 else 0  :colloumn+2 if colloumn+2 <= board.shape[1] else board.shape[1],
                        row - 1 if row - 1 > 0 else 0: row + 2 if row + 2 <= board.shape[2] else board.shape[2]]) - board[aisle,colloumn,row]


                # if the cells alive (=1) and it is  over populated or underpopulated then set the cell to dead 0
                if board[aisle,colloumn,row] == 1:

                    # if (living_neighbours < args.min_living) or (living_neighbours > args.max_living):
                    if not ( (living_neighbours >= args.min_living) and (living_neighbours <= args.max_living)):
                        coppied_board[aisle,colloumn,row]  = 0

                # if the cell is dead
                elif board[aisle,colloumn,row] == 0:

                    if ( living_neighbours <= args.max_reproduction and living_neighbours >= args.min_reproduction):

                        coppied_board[aisle,colloumn,row]  = 1
                else:
                    print("just what could have gone wrong")

    # return the coppied
    return coppied_board


def update_2d(board,width,height,wrap = True):
    """

    :param board: 2d numpy nandarray board with 1 = living cell and 0 = a dead cell
    :param width: :param height: the NXN of a single layer in the game board
    :param wrap: if True the game is seen as a spherical surfice where the game board is never ending in any direction
    :return: an updated 2D numpy ndarray after putting the original over the rules of the 2d game
    """


    # coppies the board so all boards neightbours are calculated at a static point
    coppied_board = board.copy()
    # itterates over the dimensions of the board
    for row in range (0,width):
        for colloumn in range (0,height):

            # if the boord is a square only look at the neightbours within the board
            # WARNING it is recomended that if you set wrap to false you give a slight buffer around the edge for any templates to run well
            if wrap == False:
                living_neighbours = np.sum(board[row-1:row+2,colloumn-1:colloumn+2]) - board[row,colloumn]
            # if the board is a sphere then use numpies wrap functions but still take the living neighbours like before
            elif wrap == True:
                living_neighbours = np.sum(board.take(range(row-1,row+2),mode='wrap', axis=0).take(range(colloumn-1,colloumn+2),mode='wrap',axis=1))- board[row,colloumn]
            else:
                return "Fail wrap not set correctly"

            ## if the cell is alive and they are over or underpopulated set the cell to 0
            if board[row, colloumn] == 1:
                if (living_neighbours < args.min_living) or (living_neighbours > args.max_living):
                    coppied_board[row, colloumn] = 0
            ## if the cell is dead and they have enoght living neighbours set the cell to alive

            else:
                if (living_neighbours >= args.min_reproduction) and (living_neighbours <= args.max_reproduction):
                    coppied_board[row, colloumn] = 1
    # return the new board
    return coppied_board



def twod_conways_game_of_life ():
    #define a 2D board
    board = np.zeros((args.width,args.height), dtype= int)

    # if a reference image is given then load the board from the file
    if args.filename != None:
        board = add_living_file_2d(board,args.filename)
    # if a reference image is not given then generate a random board from the random cmd lind argument

    elif (args.random>0):

        indices = np.random.choice(board.shape[1] * board.shape[0], replace=False,
                                   size=int(board.shape[1] * board.shape[0] * args.random))
        board[np.unravel_index(indices, board.shape)] = 1

    #defines a storage array for the boards, the items of this will be saved as a gif later
    board_store = []

    # if the board is set to go for a number of iterations
    if args.completion == False:

        for i in range (0,args.iterations):
            # for each iteration draw the board
            bigger_img = board.repeat(args.scale, axis=0).repeat(args.scale, axis=1)
            board_store.append(255 * bigger_img.astype(np.uint8))



            plt.imshow(update_2d(board,board.shape[0],board.shape[1], wrap = args.wrap), interpolation='nearest', origin='lower'
                       ,cmap = colors.ListedColormap(['black', 'yellow']), vmin=0, vmax=1)

            # depending on everyx show the image if the conditions are met
            # none = show the image for every iterations
            # -1 never show the image
            # any other value take the mod of the current iterationand the number of iterations and shows to screen
            # on every x itteration
            if args.everyx == None:
                plt.show()
            elif args.everyx == -1 or args.everyx == 0:
                pass
            elif i % args.everyx == 0:
                plt.show()

            # multiply the board with 255 for image saving later (we could likely have this being any value 0 - 255 to set living to a shade of grey)
            # board_store.append(255 * board.astype(np.uint8))

            # update the board
            board = update_2d(board,board.shape[0],board.shape[1], wrap = args.wrap)
    elif args.completion == True:
        count = 0

        while True:
            # same exact as above only difference is the coount variable is used for iteration number
            bigger_img = board.repeat(args.scale, axis=0).repeat(args.scale, axis=1)
            board_store.append(255 * bigger_img.astype(np.uint8))

            plt.imshow(update_2d(board,board.shape[0],board.shape[1], wrap = args.wrap), interpolation='nearest', origin='lower',
                       cmap = colors.ListedColormap(['black', 'yellow']), vmin=0, vmax=1)

            if args.everyx == None:
                plt.show()
            elif args.everyx == -1 or args.everyx == 0:
                pass
            elif count % args.everyx == 0:
                plt.show()
            copy_board = board.copy()
            board = update_2d(board,board.shape[0],board.shape[1], wrap = args.wrap)

            if (copy_board == board).all():
                break
            count +=1

    # save the list of boards as a gif
    imageio.v2.mimwrite(args.gif, board_store, format=".gif",fps = args.fps)


    return 0



def threed_conways_game_of_life():
    #define a 3D board

    board = np.zeros((args.depth,args.width,args.height), dtype= int)

    # if a reference image is given then load the board from the file


    if args.filename != None:
        board = add_living_file_3d(board,args.filename)
    # if a reference image is not given then generate a random board from the random cmd lind argument

    elif (args.random>0):
        indices = np.random.choice(board.shape[1] * board.shape[2] * board.shape[0] , replace=False,
                                   size=int(board.shape[2] * board.shape[1] * board.shape[0] * args.random))
        board[np.unravel_index(indices, board.shape)] = 1

    # some variables required for displaying the graph and for the gif
    plt.rcParams["figure.figsize"] = [5.00, 3.00]
    plt.rcParams["figure.autolayout"] = True
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.azim = 90

    # makes an image store as above
    images = []
    ax.view_init(args.elevation, 0)


    # itterates for times given by the command line argument
    for i in range(0, args.iterations):
        ax.set_xlim(0, args.width)
        ax.set_ylim(0, args.height)
        ax.set_zlim(0, args.depth)
        # set displayed graph angle to inciment by the cmd line argument
        ax.azim = ax.azim + args.azimuth_incriment

        # gets a list of x,y,z, positions where the value is not 0
        # (i.e. 3 variables to hold the coordinates of living cells)
        z, x, y = board.nonzero()

        # make the 3d scatter plot
        ax.scatter(x, y, z, c=z, alpha=1, s=10, marker="s", edgecolors="black")


        # depending on everyx show the image if the conditions are met
        # none = show the image for every iterations
        # -1 never show the image
        # any other value take the mod of the current iterations and the number of iterations and shows to screen
        # on every x iteration

        if args.gridlines == False:
            ax.axis('off')


        board = update_3d(board,board.shape[0],board.shape[1],board.shape[2])

        # draw the figure as a canvas then load the canvas as a string using numpies from 
        # buffer. so that the image in the figgur can be saved
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        
        # np from buffer gives a long 1d array of values which needs to be reshaped
        images.append(image.reshape(300, 500, 3))
        
        # clear the axis so the images dont overlay eachother
        ax.clear()

    # save the images as a gif
    imageio.v2.mimsave(args.gif, images,format = ".gif", fps=args.fps)
    return 0



if __name__ == '__main__':
    
    # directs the functions to either the 2d version of the game or 3d depending on cmd argument dimensions
    if args.dimensions == 2:
        twod_conways_game_of_life()
    elif args.dimensions == 3:
        threed_conways_game_of_life()
