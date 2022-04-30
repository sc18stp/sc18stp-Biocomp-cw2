this comes as an additional tool to go alongside the conways game of life
3d project. This is to be used to improve the ease at which one can build a
board for 3d games of life accurately.

for instilation instructions and required packages please see the main readme in the parent folder for conways
game of life. specifically note this section requires tkinter.


To run simply run:

python3 boardGen-gui.py

which will open a 2D pattern board of size 15x15.
note for the pattern boards the program requires a square board (though that can be arbitrarily deap in 3D)

#####################################################################################################################

at the top of the screen is the menu bar, under file you will see options like
New: gives a black/dead board
save: saves files to location given in --filename (defaults to current location for 3d and output.txt for 2d)
load: (not availible until a file is saved or files of the correct format are found in the local file) saves the
        coordinates of the living cells to the filename provided as filename
random: opens a popup menu to allow for the percentage of living cells you'd like in a new random board.
exit:   exits

besides the dropdown is a display function which will show the full board with yellow being alive and black being dead

under the menu bar you will find the buttons which correlate to a cell at that position. This area is the part that
takes the longest to load and comes with a scrollbar on the right hand side for both horrizontal and vertical scrolling.

by pressing on a cell you will toggle if it is living or not.

#######################################################################################################################

there is also 3 hidden features if the board is set to 2d
when toggled to 3d (instructions as to how in the command line arguments section)
a new section will be added to the bottom of the screen listing what the current layer is as well as 2 buttons at the
top of the screen which will take you forwards or backwards through the layers.


#######################################################################################################################

command line inputs

--filename (default = "./"): if set to 2D this should be a file or path to a file where you want to save the board once
            it is completed. this will save as a list of coordinates for living cells.

--width (default = 15):
--height (default = 15):    as mentioned before this assumes a square pattern so make sure both are the same. this will
                            define the perameters of the board you will be using while technically this can be set
                            arbitrarily large loading buttons in tkinter is slow and
                            at 100 x 100 you will create 10,000 buttons which even on my home pc takes a considerable
                            time (nine to ten minutes) before it displays the GUI.

--dimensions (default = 2): 2 or 3 dimentions for the board
--depth (default = 10): similar to width and height but for the z dimension. doesn't need to be equal to
                       either width or height
--random (default = 0.2): how many living cells are given onto a random new start board. this can be changed in the gui


####################################################################################################################


example command line for 50% living 3d board 10x10x10
python3 boardGen-gui.py --dimensions 3 --height 10 --width 10 --depth 10 --random 0.5

example command line for 0% living 3d board 50x50 --filename gui_example/3d_example

python3 boardGen-gui.py --dimensions 3 --height 50 --width 50  --random 0 --filename gui_example/file
######################################################################################################################
tutorial 1:
from a black board we will make and run a 3d 5766 glider starting with running the board generator:

python3 boardGen-gui.py --dimensions 3 --filename video_tutorial/board_generator/ --width 25 --height 25 --depth 15 --random 0

python3 conways.py --filename templates/video_tutorial/board_generator/ --gif templates/video_tutorial/output_gif/video_tutorial.gif --elevation 30 --dimensions 3  --width 25 --fps 5 --height 25 --depth 25 --min_reproduction 6 --max_reproduction 6 --min_living 5 --max_living 7  --iterations 60 --gridlines --azimuth_incriment 0
example video

https://youtu.be/IyvK1pNXdXo
#####################################################################################################################################

tutorial 2:

from a completely alive 2d board, clear the board and save the new board.
set 20 percent of cells to alive then run with default conways settings
(going straight to gif not showing intermediate graphs)


python3 boardGen-gui.py --filename video_tutorial/2d/video_tutorial  --width 20 --height 20 --random 1


python3 conways.py --filename templates/video_tutorial/2d/video_tutorial --width 20 --height 20 --gif templates/video_tutorial/output_gif/2d_tutorial_0.2.gif --everyx -1

the final run of the second command in the tutorial was

python3 conways.py --filename templates/video_tutorial/2d/video_tutorial --width 20 --height 20 --gif templates/video_tutorial/output_gif/2d_tutorial_0.2.gif --everyx -1 --scale 10


example video

https://youtu.be/tReyhTgrrYM
####################################################################################################################
