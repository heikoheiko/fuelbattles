from testenv import tester, logger

called_code = """
move = [1,2,3]
return(move, 3)
"""

caller_code = """
address = msg.data[0]
memory_length = 68
memory = array(memory_length)
gas = 1000
#move = call(address, memory, memory_length, 3)
move = msg(gas, address, 0, memory, memory_length, 3)
return(move, 3)
"""

s = tester.state()
c1 = s.contract(called_code, sender=tester.k0)
c2 = s.contract(caller_code, sender=tester.k0)
print logger.print_log_history(5)
move = [1, 2, 3]
r = s.send(tester.k0, c2, 0, [])
assert r == move, (r,move)


# msg(gas, to, value, datarray, insize, outsize)
#move = msg(gas, address, 0, memory, memory_length, 3)
