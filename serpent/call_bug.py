from testenv import tester, logger

code_sub = """
move = [1,2,3]
return(move, 3)
"""

"""
https://github.com/ethereum/wiki/wiki/Serpent

call(addr, datarray, insize, outsize)
equivalent to msg(tx.gas - 25, addr, 0, datarray, insize, outsize)
"""

code_call = """
address = msg.data[0]
insize = 68
outsize = 3
datarray = array(insize)
move = call(address, datarray, insize, outsize)
return(move, outsize)
"""


"""
msg(gas, to, value, datarray, insize, outsize):
sends a message with the specified recipient,
quantity of ether (in wei) and amount of gas,
taking insize values from the specified array as input,
and returns an outsize-sized data array as the output
"""

code_msg = """
address = msg.data[0]
insize = 68
outsize = 3
datarray = array(insize)
gas = 1000
value = 0
move = msg(gas, address, value, datarray, insize, outsize)
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



# fails on osx and linux
print
print "test msg()"
r = s.send(tester.k0, c3, 0, [c1.decode('hex')])
if r != move:
    print 'FAILED! %r != %r' %(r, move)
else:
    print 'PASSED'

# fails on os x passes on linux
print
print "test call()"
r = s.send(tester.k0, c2, 0, [c1.decode('hex')])
if r != move:
    print 'FAILED! %r != %r' %(r, move)
else:
    print 'PASSED'

