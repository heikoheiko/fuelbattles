from colorconsole import terminal
import time

green, red, black = (terminal.colors[x] for x in ('GREEN', 'BLUE', 'BLACK'))

def draw(sim_steps, cols, rows, a_grid, b_grid, redistribution_grid):
    screen = terminal.get_terminal(conEmu=False)
    if sim_steps == 0:
        screen.clear()
    screen.gotoXY(0, 0)
    a_fuel = sum(a_grid)
    b_fuel = sum(b_grid)
    print "STEP:%d\tFUEL: A:%d\tB:%d\tA+B:%d" % (sim_steps, a_fuel, b_fuel, a_fuel + b_fuel)

    y_offset = 10
    norm = 99. / max(a_grid + b_grid)
    for row in range(rows):
        for col in range(cols):
            idx = row * cols + col
            owner = '   '
            r = hex(redistribution_grid[idx] / 16)[-1]
            #r = '%3d' % redistribution_grid[idx]
            if a_grid[idx]:
                owner = '%2d' % (a_grid[idx] * norm)
            if b_grid[idx]:
                owner = '%2d' % (b_grid[idx] * norm)
            screen.gotoXY(1+ col*3, y_offset + row)
            if a_grid[idx]:
                c = red
            elif b_grid[idx]:
                c = green
            else:
                c = black
            screen.xterm256_set_bk_color(c)
            print owner,
        print
    screen.xterm256_set_bk_color(black)
    time.sleep(.04)

import simulator
simulator.debug_callback = draw