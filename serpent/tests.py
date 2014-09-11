# not really py.test but used for testing while development

from testenv import tester
from testenv import run, logger


def test_organizer():
    s = tester.state()
    simulation = s.contract('simulaton.se')
    print "simulator: %s" % simulation
    organizer = s.contract('organizer.se')
    ai_address = organizer
    print "organizer: %s" %  organizer
    stake = 10**6
    simulation_gas = 10**5

    # send bets send(sender, to, value, data=[])
    print 'tx1:', s.send(tester.k0, organizer, stake, data=[ai_address, simulation_gas])
    print 'tx2:', s.send(tester.k1, organizer, stake, data=[ai_address, simulation_gas + 2000])



def test_get_neighbours():
    s = tester.state()
    c = s.contract('get_neighbours.se')
    r = s.send(tester.k0, c, 0, data=[4, 3, 3])
    expected = [4, 1, 7, 3, 5] # num, n0, n1, ...
    assert r == expected, (r, expected)
    r = s.send(tester.k0, c, 0, data=[8, 3, 3])
    expected = [2, 5, 7, 0, 0]
    assert r == expected, (r, expected)
test_get_neighbours()


def test_is_neighbour():
    s = tester.state()
    c = s.contract('is_neighbour.se')
    for expected, a, b in [(0, 1, 1), (1, 0, 1), (1, 4, 7), (0, 4, 8)]:
        assert [expected] == s.send(tester.k0, c, 0, data=[a, b, 3, 3])
test_is_neighbour()


def test_debug():
    s = tester.state()
    debug = s.contract('debug.se')
    print "debug address: %s" % debug
    print s.send(tester.k0, debug, 0, data=["hallo", 1, 2, 3])
    print 'debug returned'
test_debug()



def redistribution_grid(seed, ncells):
    def _sort(data):
        s = []
        i = 0
        while i < ncells:
            s.append((data[i*2], data[i*2+1]))
            i +=1
        s.sort()
        r = []
        for v,c in s:
            r.extend([v,c])
        return r

    i = 0
    redistribution_grid = [0] * (ncells * 2)
    while i < ncells/2:
        v = (seed / (i+1) % 256)
        redistribution_grid[i*2] = v
        redistribution_grid[i*2+1] = i
        redistribution_grid[ncells * 2 - (i+1)*2] = v
        redistribution_grid[ncells * 2 - (i+1)*2 + 1] = ncells - i - 1
        i += 1
    sg = _sort(redistribution_grid)
    i = 0
    while i < ncells:
        v = sg[i*2]
        c = sg[i*2+1]
        redistribution_grid[i * 2] = v
        redistribution_grid[i * 2 + 1] = c
        i += 1
    return redistribution_grid

#print redistribution_grid(4324211223, 16)

tester.gas_limit = 10**5 - 10**4

def test_ai_simple():
    s = tester.state()
    print "setting up ai_simple"
    a_ai = s.contract('ai_simple.se')
    print "SETUP GAS", s.block.gas_used
    print "GAS LIMIT", s.block.gas_limit
    b_ai = 2
    cols, rows = 4, 4
    a_grid = [0] * cols*rows
    b_grid = [0] * cols*rows
    a_grid[2], b_grid[-2-1] = 1000, 1000
    msgdata = [cols, rows, a_ai.decode('hex'), b_ai] + a_grid + b_grid + redistribution_grid(319283098, cols*rows)
    print msgdata
    r = s.send(tester.k0,a_ai, 0, data=msgdata)
    print r

test_ai_simple()

def test_simluation_setup():
    s = tester.state()
    simulation = s.contract('simulation.se')
    logger.register_address('sim', simulation)
    a_ai = s.contract('ai_simple.se')
    logger.register_address('a_ai', a_ai)
    b_ai = s.contract('ai_two.se')
    logger.register_address('b_ai', b_ai)
    try:
        print s.send(tester.k0, simulation, 0, data=[a_ai, b_ai])
    except Exception, e:
        print '\n'.join(repr(x) for x in logger.get_history(1))
        raise e
test_simluation_setup()

def test_quicksort():
    s = tester.state()
    c = s.contract('quicksort_pairs.se')
    data = [ 30, 1, 90, 2, 70, 3, 50, 4]
    expected = [ 30, 1, 50, 4, 70, 3, 90, 2 ]
    r = s.send(tester.k0, c, 0, data=data)
    assert expected == r, (r, expected)
test_quicksort()


