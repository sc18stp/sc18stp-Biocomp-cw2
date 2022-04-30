import numpy as np
import argparse
from matplotlib import pyplot as plt
import os

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt

def update_3d(board,width,height,depth):
    coppied_board = board.copy()
    count = -1
    for row in range (0,width):
        for colloumn in range (0,height):
            for aisle in range (0,depth):
                count +=1
                # print (count)
                # print(row)
                # print (colloumn)
                # print (aisle)

                living_neighbours = np.sum(np.array([x.take(range( row - 1,  row+ 2), mode='wrap', axis=0).take(range( colloumn - 1,  colloumn + 2), mode='wrap',axis=1) for x in board])) - board[row,colloumn,aisle]
                # print (living_neighbours)
                # print( board[row, colloumn,aisle] == 1)

                if board[row, colloumn,aisle] == 1:
                    if (living_neighbours < 2) or (living_neighbours > 3):
                        coppied_board[row, colloumn,aisle] = 0
                else:
                    if living_neighbours == 3:
                        coppied_board[row, colloumn,aisle] = 1


    return coppied_board


def rle_template_reader(board, file):
    read = open(file, "r")
    for line in read.readlines():
        if line[0] != "#":
            if line[0] == "x":
                split_by_command = line.split(",")
                # if the integer componant of the command x = OO of the rle file is greater then the board dimmentions error
                assert (int(split_by_command[0].split("=")[1]) <= args.width)
                # if the integer componant of the command x = OO of the rle file is greater then the board dimmentions error
                assert (int(split_by_command[1].split("=")[1]) <= args.width)
                print(split_by_command)
            line = -1

            for array_line in line.split("$"):
                line += 1
                EndOfLine = False
                while EndOfLine != True:
                    offset_from_0 = 0
                    if array_line == "!":
                        return board
                    if array_line.find("b") < array_line.find("o"):
                        b_index = array_line.find("b")
                        offset_from_0 += b_index

    return board


if __name__ ==  '__main__':
    string = "3bob$4bo"



    #
    # # board = np.array([[[0,1,2],[3,4,5],[6,7,8]],[[9,10,11],[12,13,14],[15,16,17]],[[18,19,20],[21,22,23],[24,25,26]]])
    # # print([x.take(range( - 1,  + 2), mode='wrap', axis=0).take(range( - 1,  + 2), mode='wrap',axis=1) for x in board])
    # #
    # # plt.rcParams["figure.figsize"] = [7.00, 3.50]
    # # plt.rcParams["figure.autolayout"] = True
    # # fig = plt.figure()
    # # ax = fig.add_subplot(111, projection='3d')
    # # # print(len (board.nonzero()[0]))
    # # # print(i)
    # # # ax.view_init(0,0)
    # # z, x, y = board.nonzero()
    # #
    # # ax.scatter(x, y, z, c=z, alpha=1, s=10, marker="s", edgecolors="black")
    # # # plt.grid()
    # # plt.show()
    #
    # # # nnumpy_array = np.array([[0,1,2],[3,4,5],[6,7,8]])
    # # # print (nnumpy_array)
    # # # print (nnumpy_array.take(range(-1,2),mode='wrap', axis=0).take(range(-1,2),mode='wrap',axis=1))
    # # # array = [[0,1,2],[3,4,5],[6,7,8]]
    # # # array_1d = [0,1,2,3]
    # # # print(array_1d[:-1])
    # # #
    # # # board = np.zeros((50,50), dtype= int)
    # # # file = open("templates/dozen_pulser.csv","r")
    # # # for row, line in enumerate(file.readlines()):
    # # #     line_array = np.array(list(map(int,  line.split(","))))
    # # #     print (np.sum(board))
    # # #     for colloumn in np.where(line_array == 1):
    # # #         board[row,colloumn] =1
    # # # print(board)
    # # fig = plt.figure()
    # # print(np.where(board == 1))
    # # index = np.where(board == 1)
    # # outfile = open("dozen_pulser.txt","w")
    # # for x in range (0,len(np.where(board == 1)[0])):
    # #     print(str(index[0][x])+","+str(index[1][x]))
    # #
    # #     print(board[index[0][x],index[1][x]])
    # #     outfile.write(str(index[0][x])+","+str(index[1][x])+"\n")
    # #     # print (board[x,y])
    # # exit(10)
    # # plt.imshow(board, interpolation='nearest')
    # # plt.show()
    # # copy_board = board.copy()
    # list_of_files = [x for x in os.listdir("templates") if x.endswith(".txt") and x[:-4].isnumeric() and int(x[:-4]) >= 0]
    # print(list_of_files)
    #
    # board = np.zeros((10,25,25), dtype = int)
    #
    #
    # for filename in list_of_files:
    #     print(filename)
    #     file = open("templates/"+filename,"r")
    #     for row, line in enumerate(file.readlines()):
    #         line_array = np.array(list(map(int,  line.split(","))))
    #         print(line_array)
    #
    #
    #         # print (np.sum(board))
    #         for colloumn in np.where(line_array == 1):
    #             print(str(row)+ "," + str(colloumn))
    #             board[int(filename[:-4]),row,colloumn] =1
    #     print(board[int(filename[:-4])])
    # plt.rcParams["figure.figsize"] = [7.00, 3.50]
    # plt.rcParams["figure.autolayout"] = True
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # # print(len (board.nonzero()[0]))
    # # print(i)
    # # ax.view_init(0,0)
    # z, x, y = board.nonzero()
    #
    # ax.scatter(x, y, z, c=z, alpha=1, s=10, marker="s", edgecolors="black")
    # # plt.grid()
    # plt.show()
    # print(board)
    # for inte in range (0,400):
    #     board = update_3d(board, board.shape[0], board.shape[1], board.shape[2])
    #     print(board)
    #
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')
    #         # print(len (board.nonzero()[0]))
    #         # print(i)
    #         # ax.view_init(0,0)
    #     z, x, y = board.nonzero()
    #
    #     ax.scatter(x, y, z, c=z, alpha=1, s=10, marker="s", edgecolors="black")
    #         # plt.grid()
    #     plt.show()
