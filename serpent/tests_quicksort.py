# not really py.test but used for testing while development

from testenv import tester
from testenv import run, logger

def test_quicksort():
    s = tester.state()
    c = s.contract('quicksort_pairs_debug.se')
    logger.register_address('qsort', c)
    data = [ 30, 1, 90, 2, 70, 3, 50, 4]
    expected = [ 30, 1, 50, 4, 70, 3, 90, 2 ]
    print 'sorting', data
    r = s.send(tester.k0, c, 0, data=data)
    assert expected == r, (r, expected)
test_quicksort()


