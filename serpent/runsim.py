# execute this to run a battle
from testenv import tester
from testenv import run, logger
tester.gas_limit = 10**5 - 10**4

def print_log_history(num):
    print '\n'.join(repr(x) for x in logger.get_history(num))

def run_simulation():
    s = tester.state()
    simulation = s.contract('simulation.se')
    logger.register_address('sim', simulation)
    a_ai = s.contract('ai_simple.se')
    logger.register_address('a_ai', a_ai)
    b_ai = s.contract('ai_simple.se')
    logger.register_address('b_ai', b_ai)
    winner = s.send(tester.k0, simulation, 0, data=[a_ai, b_ai])
    try:
        if not winner:
            print 'simulation failed'
            print print_log_history(2)
        elif winner[0] == a_ai.decode('hex'):
            print "A wins"
        else:
            print "B wins"
        print logger.get_history()

    except Exception, e:
        print_log_history(2)
        raise e

if __name__ == '__main__':
    run_simulation()
