# execute this to run a battle
from testenv import tester
from testenv import run, logger
tester.gas_limit = 10**5 - 10**4

def run_simulation():
    s = tester.state()
    simulation = s.contract('simulation.se')
    logger.register_address('sim', simulation)
    a_ai = s.contract('ai_simple.se')
    logger.register_address('a_ai', a_ai)
    b_ai = s.contract('ai_two.se')
    logger.register_address('b_ai', b_ai)
    try:
        winner = s.send(tester.k0, simulation, 0, data=[a_ai, b_ai])
        if winner[0] == a_ai.decode('hex'):
            print "A wins"
        else:
            print "B wins"
        print logger.get_history(2)[-2]

    except Exception, e:
        print '\n'.join(repr(x) for x in logger.get_history(1))
        raise e

if __name__ == '__main__':
    run_simulation()
