# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Go through all the units and check for the existence of same value in multiple boxes in each units.

   If the same value exists within the unit, then check the length of the values with the number of boxes found with that value. If both the lengths are same, then remove the digits of this value from the values of other boxes of that unit. Ex - if the value of a box is '23', then naked twins will try to find the value '23' in other boxes within that unit and if found then the value '23' should be present only in 2 boxes within that units. Then eliminate the digits 2&3 from values of the other boxes in the unit. 

   Similarly if the value of a box is '123', then naked twins will try to find the value '123' in other boxes within that unit and if found then the value '123' should be present only in 3 boxes within that units which is equal to the length of the value. Then eliminate the digits 1,2,3 from values of the other boxes in the unit. 


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In addtion to the normal elimination rules where the value will be eliminated from all it peers(Row Unit, Column Unit and 3x3 square unit), for   
   the diagonal sudoku if the box is a part of the Major Diagonals, then also eliminate the value(single digit) from the values of all its peers along that diagonal. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.