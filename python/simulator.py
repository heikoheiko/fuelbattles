import sha3
from common import get_neighbours, mk_redistribution_grid
debug_callback = None

inv_redistribution_factor = 25
cols = 6
rows = 6


def call(a_address, b_address, a_ai, b_ai, start_gas):
    a_fuel = start_gas / 2
    b_fuel = start_gas / 2

    # setup grid
    ncells = cols * rows
    a_grid = [0] * ncells
    b_grid = [0] * ncells

    # redistribution grid
    seed = id(a_address) # prevhash
    seed = sha3.sha3_256(str(seed)).digest()
    redistribution_grid = mk_redistribution_grid(seed, ncells)

    # place a, b
    pos = ord(seed[0]) % (ncells/2)
    a_grid[pos] = a_fuel
    b_grid[-pos-1] = b_fuel


    def is_neighbour(a, b):
        return b in get_neighbours(a, cols, rows)

    def validate_move(grid, from_cell, to_cell, fuel):
        # check within grid
        if from_cell < ncells:
            if to_cell < ncells:
                # enough fuel there
                if fuel <= grid[from_cell]:
                    # check neighbour
                    if is_neighbour(from_cell, to_cell):
                        return True
        return False

    def total():
        return sum(a_grid + b_grid)

    sim_step_gas = 0
    sim_steps = 0
    total_gas_used = 0

    # end if one ran out of gas or half of start_gas is used
    while a_fuel > 0 and b_fuel > 0 and total() > start_gas / 2:
        if debug_callback:
            debug_callback(sim_steps, cols, rows, a_grid, b_grid, redistribution_grid)

        total_at_start = total()
        redistribution = 0

        for ai, grid, other_grid, fuel in ((a_ai, a_grid, b_grid, a_fuel), (b_ai, b_grid, a_grid[:], b_fuel)): # copy a_grid for 2nd call
            gas_used, move_from, move_to, move_amount = ai(seed, cols, rows, grid, other_grid)

            total_gas_used += gas_used
            if move_amount and not validate_move(grid, move_from, move_to, move_amount):
                move_amount = 0

            # move
            if move_amount:
                grid[move_from] = grid[move_from] - move_amount
                grid[move_to] = grid[move_to] + move_amount

            # remove gas and redistribution
            for i in range(ncells):
                cell_fuel = grid[i]
                redistribution_allowance = cell_fuel / inv_redistribution_factor
                gas_allowance = (sim_step_gas / 2 + gas_used) * cell_fuel / fuel
                grid[i] = max(0, cell_fuel - gas_allowance - redistribution_allowance)
                redistribution = redistribution + redistribution_allowance


        # handle collisions
        for i in range(ncells):
            if a_grid[i] and b_grid[i]:
                if a_grid[i] > b_grid[i]:
                    g, l = a_grid, b_grid
                else:
                    l, g = a_grid, b_grid
                d = g[i] - l[i]
                g[i] -= d
                l[i] = 0
                redistribution += d

        a_fuel = 0
        b_fuel = 0

        rnorm = sum(r for i, r in enumerate(redistribution_grid) if a_grid[i] or b_grid[i])

        for i in range(ncells):
            add = redistribution * redistribution_grid[i] / rnorm
            if a_grid[i]:
                a_grid[i] += add
            if b_grid[i]:
                b_grid[i] += add
            a_fuel += a_grid[i]
            b_fuel += b_grid[i]

        assert total_at_start > total()

        sim_step_gas = 3000 # guess
        total_gas_used += sim_step_gas
        sim_steps += 1

    # end while loop
    winner = a_address if a_fuel > b_fuel else b_address
    return total_gas_used, winner
