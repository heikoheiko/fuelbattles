from testenv import tester, logger

code_sub = """
move = [1,2,3]
return(move, 3)
"""

code_call = """
address = msg.data[0]
memory_length = 68
memory = array(memory_length)
move = call(address, memory, memory_length, 3)
return(move, 3)
"""

code_msg = """
address = msg.data[0]
memory_length = 68
memory = array(memory_length)
gas = 1000
value = 0
move = msg(gas, address, value, memory, memory_length, 3)
return(move, 3)
"""


print 'setting up contracts',
s = tester.state()
logger.register_address('EOA', tester.a0)

c1 = s.contract(code_sub, sender=tester.k0)
logger.register_address('code_sub', c1)

c2 = s.contract(code_call, sender=tester.k0)
logger.register_address('code_call', c2)

c3 = s.contract(code_msg, sender=tester.k0)
logger.register_address('code_msg', c3)



move = [1, 2, 3]


# test msg_code
print
print "test msg()"
r = s.send(tester.k0, c3, 0, [c1.decode('hex')])
if r != move:
    print 'FAILED! %r != %r' %(r, move)


# test caller_code
print
print "test call()"
r = s.send(tester.k0, c2, 0, [c1.decode('hex')])
if r != move:
    print 'FAILED! %r != %r' %(r, move)

