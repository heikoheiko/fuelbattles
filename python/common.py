def mk_redistribution_grid(seed, ncells):
    redistribution_grid = [0] * ncells
    weights = [ord(c) for c in seed[:ncells/2]]
    #weights = range(ncells/2)
    for i, v in enumerate(weights):
        redistribution_grid[i] = v
        redistribution_grid[-i-1] = v
    return redistribution_grid

def get_neighbours(a_cell, cols, rows): #
    hood = []
    a_col = a_cell % cols
    a_row = a_cell / cols

    if a_row > 0:
        hood.append(a_cell - cols)
    if a_row < rows - 1:
        hood.append(a_cell + cols)
    if a_col > 0:
        hood.append(a_cell - 1)
    if a_col < cols -1:
        hood.append(a_cell + 1)
    return hood

assert get_neighbours(4, 3, 3) == [1, 7, 3, 5]
assert get_neighbours(8, 3, 3) == [5, 7]
