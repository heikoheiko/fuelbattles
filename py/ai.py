from common import mk_redistribution_grid, get_neighbours

def ai_one(seed, cols, rows, grid, other_grid):
    "goes to the best reachable sources"
    redistribution_grid = mk_redistribution_grid(seed, cols * rows)
    # cells sorted by redust
    targets = sorted(range(cols * rows), key=lambda i: redistribution_grid[i], reverse=True)
    for i, cell in enumerate(targets):
        if grid[cell]: # here already
            continue
        # check if it's reachable
        for n in get_neighbours(cell, cols, rows):
            if grid[n] > 1: # match
                gas_used = i * 10 * 8
                # move half of funds at cell
                return gas_used, n, cell, grid[n]/2
    #  none move
    return (i+cell) * 10 * 9,  0, 0, 0


def ai_two(seed, cols, rows, grid, other_grid):
    "goes to the best reachable sources if it can win the fight about an occuppied cell"
    redistribution_grid = mk_redistribution_grid(seed, cols * rows)
    targets = sorted(range(cols * rows), key=lambda i: redistribution_grid[i], reverse=True)
    # cells sorted by redistribution
    for i, cell in enumerate(targets):
        if grid[cell]: # here already
            continue
        # check if it's reachable
        for n in get_neighbours(cell, cols, rows):
            # check whether we should attack
            if other_grid[cell] and other_grid[cell] > grid[n]:
                continue
            if grid[n] > 1: # match
                if other_grid[cell]:
                    moved_fuel = max(grid[n] - other_grid[cell], grid[n]/2)
                else:
                    moved_fuel = grid[n]/2
                gas_used = i * 10 * 9
                return gas_used, n, cell, moved_fuel
    # none move
    return (i+cell) * 10 * 9,  0, 0, 0
