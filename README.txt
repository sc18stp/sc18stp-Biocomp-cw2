2 example videos are provided in the templates readme file above the instructions for the boardGen-gui.py
conways.py
###############################################################
instillation and Compilation:

Instilation should be simple assuming pip and python are already installed. The only None simple requirement is
tkinter which might need to be installed with sudo privileges, but it is also often packaged with python depending
on the instillation method. On Linux you can use:

sudo apt-get install python3-tk

other then that once in either function folder (the root or /templates) run:

pip3 install requirements.txt

################################################
As for running instructions to run an example of a random 15x15 2D board use:

python3 conways.py

further instructions follow. To run the same example without displaying every update use:

python3 conways.py --everyx -1

or:

python3 conways.py --everyx 0

for more information on other arguments read on
#########################################################################
Introduction
Conway’s game of life is a zero player game played on an infinite board.
Zero player means the game takes an initial condition and can not be effected until the game is finished and instead
the game is played by the computer following a set of rules until completion. The 2D version of the game was also proved
to be universal/Turing complete cellular automata, proved by Paul Rendell  who implemented a Turing complete machine in
2000 with signals and gates made from gliders/ants (first discovered by Richard k. Guy) in 1969. Subsequently, Bill
Gosper only one year later in 1970 made the first infinitely spawning arrangement in the Gosper Gun being a p = 30 gun
that fires a new ant every 30 periods wining $50 from Conway and being the basis of proving the universality of the game.

For the Conway’s version of the game of life there are 3 main rules
1. any living cell which is alive with less than 2 neighbours dies of underpopulation/loneliness
2. any living cell which is alive with more than 3 neighbours dies of overpopulation/lack of resources
3. any dead cell with 3 living neighbours becomes alive as if from reproduction

in the official notation Conway’s game of life can be given as B3/S23 meaning a cell is born with 3 neighbours and the
cell survives with 2 or 3 neighbours.
these rules can also be written as B33/S23 meaning a child is born with between 3 and 3 neighbours.
this will be more important when looking at 3d boards where they found it is unlikely that a 3D Game of Life equivalent
with the same rules would likely not be Turing complete and therefore attention fell to changing those rules to allow for
the spawning of gliders and other key structures.

###########################################################################

File Types:

there is no official file type for Conway’s game of life since it originated as a mathematical pen and paper problem
which spawned Conway’s regret as to calling the simple pattern the glider instead of the ant. For this reason several
possible file conventions were spawned including the .cells format. This format uses an “!” character to mark lines
which consist of comments.

In these comments are often the name of the pattern, author and description of the pattern. For example:
“
!Name: Glider
!Author: Richard K. Guy
!The smallest, most common, and first discovered spaceship.
!www.conwaylife.com/wiki/index.php?title=Glider
”
in the case of the wiki a link to the pattern itself is also added followed by the pattern itself.
A living cell is marked by a “O” while a preceding dead cell is marked with a “.”. Additionally, each line doesn’t need
to have the same number of characters so the line ends with the final O and padded with dead cells until the end. Take
for example the simplest spaceship
“
.O
..O
OOO
”

This version of the game of life set out to solve a problem with most 3D implementations. And, that is the poor way the
base case is often given, either by giving the coordinates of by clicking and the program having to guess the depth as
to where you want the living cell. In this case a separate file creation method is given where a file is the same as for
a 2d board but is stored as a set of folders given by n._ _ _ where n is the layer in the 3d board the pattern refers to.

This can accept both .cells files and a .txt file consisting of (x,y) coordinates for an example see:
templates/examples/blowup/
 which demonstrates a simple 7 cell pattern starting at the arbitrary layer 22.

along with this I provide a GUI in the templates' folder to generate said folders (with a separate readme for it)
WARNING while the GUI can be run for an arbitrarily large board a 100 x 100 board can take unto 10 minutes on my home pc
 (which is admittedly above average). Additionally pattern files can be run on boards larger than themselves the height
 width provided just limit the number of buttons generated which takes the most time.





#############################################################################
example command lines = for every command line output there is an example output in the output_gifs folder so you
don’t need to run the code

base case: (saved as no_arguments.gif) for consistency an np seed is given in conway.py remove for more random boards

Python3 conways.py


###################################################################################
ant 2D examples:

python3 conways.py --filename templates/examples/ant.cells --everyx -1 –scale 10 –gif output_gifs/ant.gif

python3 conways.py --filename templates/examples/ant.cells --everyx -1 –scale 10 –gif output_gifs/scaledant.gif


python3 conways.py --filename templates/examples/ant.cells --everyx -1 –scale 10 –gif output_gifs/scaledantwraping.gif


######################################################################

ant Gosper gun 2D examples:

python3 conways.py  --filename templates/examples/glider.cells --everyx 0 --width 50 --height 50 --iterations 300 --scale 10 --fps 30 --gif output_gifs/glider_gun.gif

ant Gosper gun 2D examples (with wrap around):

python3 conways.py  --wrap --filename templates/examples/glider.cells --everyx 0 --width 50 --height 50 --iterations 300 --scale 10 --fps 30 --gif output_gifs/self_destructing_glider_gun.gif

###############################################################################

filename 2D examples:
python3 conways.py --width 50 --height 50 --scale 10 --fps 15 --filename templates/examples/pulser.cells  --everyx -1 --gif output_gifs/2dpulser.gif

occalator  3D examples:

python3 main.py --filename templates/examples/blowup  --everyx -1 --max_living 5 --min_living 5 --min_reproduction 4 --max_reproduction 5 --depth 9 --width 50 --height 50 --depth 50 --dimensions 3 --iterations 50  --gif  output_gifs/blowup.gif

<- a long form stored gif of this is saved as blow_up_example.gif
python3 main.py --filename templates/examples/blowup  --everyx -1 --max_living 5 --min_living 5 --min_reproduction 4 --max_reproduction 5 --width 100 --height 100 --depth 100 --dimensions 3 --iterations 600  --gif  output_gifs/blowup.gif

glider 3d example

python3 conways.py --filename templates/examples/glider5766/  --elevation 60 --dimensions 3  --width 20 --fps 1 --height 20 --depth 15 --min_reproduction 6 --max_reproduction 6 --min_living 5 --max_living 7  --iterations 60 --gridlines --azimuth_incriment 90 --gif output_gifs/3dglider.gif

################################################################################


Implementation

To run the basic Game of Life (GoL) run

“Python3 conways.py” from the command line will run the game with the default settings. You will see a matplotlib
graph displayed which (if closed) will then update the board and display it again.

If GoL is run with the “--help” command the full list of command line inputs (CLIs) will be displayed, with the range
of values accepted and their default values. The following document will not follow the order of the command line inputs
as given in the help documentation and will instead be given in order of usefulness.

--everyx (default = None)
everyx referes to how frequently the function will display the board depending on the value given. If None is given (i.e.
 the variable isnt set in the command line) then the board will be shown at every iteration. While this was useful when
 testing the board generated correctly now that has been confirmed closing the additional windows is not as useful. If
 this is set to a value greater then 0 then the board will only be displayed everyx iterations (though it will still be
 saved at the end).
Instead everyx can be set to -1 to not display the steps in the middle and to instead only give the final gif at the end.

--scale (default = 1)
by default each image in the 2d gif has the board taken as if each living cell is one pixel. This may be useful for
large image however for small details can often be harder to see. In this case the size of scale might be arbitrarily
large but for the sake of keeping ensuring an acceptable runtime there is a limit to a scale factor of 25. for an
example of how this looks see 100x100x100random0scale.gif and 100x100x100random10scale.gif in the output_gifs folder
which both use a 100x100 2D board for 100 iterations on the same seed.

--fps (default = 5)
Again with functions that effect the output generation, defining how quickly the frames should be pieced together to
make the gifs. Higher values make the animation smoother and the animation shorter but lower values give more time to
see the cells per iteration

see 100x100x100random10scalefps5.gif and 100x100x100random10scalefps60.gif in the output_gifs folder for a demonstration

--gif (default = output.gif)
this gives the function the file path to where you would like the gif saved. You can also give the gif a name her,
 always remember to end the filename with “.gif” to prevent corruption

--width (default = 15); --height (default = 15); --depth (default = 15);
a game board is defined by a width and a height defaulted to 15 pixels however this can be changed by typing
--width 20 --height 20. Technically any value can be given here though a limit of 250 has been imposed
for efficiency reasons. The third perimeter here defines how many width x height boards are used to make a 3D board.



--dimensions (default = 2)
dimensions defines weather the game will be run in 2D or 3D

--filename (default = None)
for 2D grids a filename should point to either a .txt or .cells file which.
For 3D grids the filename should instead point to a folder/directory containing .txt or .cells files.
In said directory the files should be named n.txt or n.cells where n refers to the layer in the board.
For example 0.cells should give the expected value for the 0th layer and 1.cells should give the living cells of the
 first layer.

Example 2D filename
filename 3D examples

--iterations (default = 100)
iterations as the name suggests defines the number of times the board is updated before the game finishes,
this is ignored in the case of --completion being set

--completion
completion was a tool during making that let the function run and repeat in 2D until two consecutive boards are the same,
 this clearly falls short if there is an oscillator however this can still stop the function early or later then a
 manually given iteration count

--wrap
 makes the flat board into a 3d sphere or to make all edges wrap around. In the case of some cells files it is
 recommended to enable --wrap or manually add an area of above and to the left of the cells file since the cells file
 might give a pattern too close to the edge and make them non-functioning.

--random (default = 0.2)
give the percentage as a decimal for how many of the cells should be living. 0 = all cells are dead 1 = all cells are
alive


--min_living(default = 2)
--max_living(default = 3)
--min_reproduction(default = 3)
--max_reproduction (default = 3)
the following 4 command line arguments give the rules of the game, for example
S {min_living,max_living} / b {min_reproduction,max_reproduction}
for the game of life this is S{2,3}/ B{3,3}


3D files

the following arguments are needed for the gif generation of the 3d board alone,
--gridlines
grid lines adds grid lines around the plot in the gif, this might be useful to gauge where cells are but in the most
case they were found to be confusing so were removed by default

when outputting the gif defines the elevation in degrees above the origin. And, the azimuth – the values in degrees
around the z axis with the origin at the centre - to be incriminated at each stage,   thus adding a spin to the gif
allowing for a wider range of angles to see the 3d plot at

