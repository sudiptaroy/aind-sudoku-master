assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        box: the box to which the new value will be assigned
        value: new value which will be assigned

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    Returns:
        the cross product of two input elements
    """
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

# Identify all the boxes in the sudoku board
boxes = cross(rows, cols)

# List of all the Row Units, Column Units and 3x3 Square Units
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Identification of the boxes for two major diagonal units
diag_units_lr = [unit[0] for unit in [cross(r,c) for r,c in zip(rows,cols)]]
diag_units_rl = [unit[0] for unit in [cross(r,c) for r,c in zip(rows,reversed(cols))]]


# Identify all the peers for all the boxes and create a dictionary for the same
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy. 
    Go through all the units and check for the existence of same value of multiple boxes in each units.

    If the same value exists within the unit, then check the length of the values with the number of boxes found with that value. If both the lengths are same,
    then replace the digits of this value from other boxes of that unit. Ex - if the value of a box is '23', then naked twins will try to find 
    the value '23' in other boxes within that unit and if found then the value '23' should be present only in 2 boxes within that units. Then eliminate
    the value from values of the other boxes in the unit. 

    Similarly if the value of a box is '123', then naked twins will try to find the value '123' in other boxes within that unit and 
    if found then the value '123' should be present only in 3 boxes within that units which is equal to the length of the value. Then eliminate
    the value from values of the other boxes in the unit. 

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        for box in unit:
            box_value = values[box]
            dplaces = [box for box in unit if values[box]==box_value]
            if(len(dplaces)>1 and len(dplaces)==len(box_value)):
                other_boxes = [box for box in unit if values[box]!=box_value]
                for other_box in other_boxes:
                    for digit in box_value:
                        assign_value(values, other_box, values[other_box].replace(digit,''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.

    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    
    In addtion to the normal elimination rules, for diagonal sudoku if the box is a part of the Major Diagonals, then also eliminate 
    the value(single digit) from the values of all its peers along that diagonal.
    Args: 
        values(dict): A sudoku grid in dictionary form.

    Returns: 
        The resulting sudoku grid in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            #values[peer] = values[peer].replace(digit,'')
            assign_value(values, peer, values[peer].replace(digit,''))
        
        diag_unit = True if box in diag_units_lr else False
        if diag_unit:
            for peer in diag_units_lr:
                if len(values[peer])>1:
                    #values[peer] = values[peer].replace(digit,'')
                    assign_value(values, peer, values[peer].replace(digit,''))

        diag_unit = True if box in diag_units_rl else False
        if diag_unit:
            for peer in diag_units_rl:
                if len(values[peer])>1:
                    #values[peer] = values[peer].replace(digit,'')
                    assign_value(values, peer, values[peer].replace(digit,''))
    
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Args: 
        values(dict): A sudoku grid in dictionary form.

    Returns: 
        The resulting sudoku grid in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Args: 
        values(dict): A sudoku grid in dictionary form.
    
    Returns: 
        The resulting sudoku grid in dictionary form if the sudoku is solved or the sudoku remains same after an iteration.
        Returns false if there is a box with no available values
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku. This serach will be recursively called until
    the sudoku is resolved
    Args: 
        values(dict): A sudoku grid in dictionary form.
    
    Returns: 
        The resulting sudoku grid in dictionary form if the sudoku is solved 
        Returns false if there is a box with no available values
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurssion to solve each one of the resulting sudokus 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solved_values = search(values)
    return solved_values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
