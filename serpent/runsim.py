# execute this to run a battle
import sys
from testenv import tester
from testenv import logger


SIM_GAS = 10**7

def run_simulation():
    s = tester.state()
    s.block.gas_limit = SIM_GAS * 2
    tester.gas_limit = SIM_GAS
    simulation = s.contract('simulation.se')
    logger.register_address('sim', simulation)
    a_ai = s.contract('ai_simple.se')
    logger.register_address('a_ai', a_ai)
    b_ai = s.contract('ai_two.se')
    #b_ai = s.contract('ai_simple.se')
    logger.register_address('b_ai', b_ai)

    try:
        winner = s.send(tester.k0, simulation, 0, data=[a_ai, b_ai])
    except Exception as e:
        logger.print_log_history(4)
        raise e

    if not winner:
        print 'simulation failed, last logs:'
        print logger.print_log_history(2)
    elif a_ai in hex(winner[0]):
        print "A WINS " * 5
    else:
        assert b_ai in hex(winner[0])
        print "B WINS " * 5

if __name__ == '__main__':
    if len(sys.argv) == 2: # debug
        run_simulation()
    else:
        import visualizer
        run_simulation()
