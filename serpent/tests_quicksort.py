# not really py.test but used for testing while development

from testenv import tester
from testenv import run, logger

s = tester.state()
c = s.contract('quicksort_pairs_debug.se')
logger.register_address('qsort', c)

def test_quicksort(data, expected):


    print 'testing', data, expected
    r = s.send(tester.k0, c, 0, data=data)
    assert expected == r, (r, expected)

test_quicksort([30, 1],[30, 1])
test_quicksort([30, 1, 20, 2],[20, 2, 30, 1])
test_quicksort([30, 0, 20, 2],[20, 2, 30, 0])
test_quicksort([30, 1, 90, 2, 70, 3, 50, 4],[ 30, 1, 50, 4, 70, 3, 90, 2 ])


