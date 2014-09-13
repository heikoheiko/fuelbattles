"""
Uses the processblock loghandler to intercept debug messages from within runing EVM code
use with debug.se, linked by 0xdeba6 in the first word of call data going to debug.se
"""
import os
import string
import pyethereum
import serpent
tester = pyethereum.tester

class Logger(object):

    debug_contract = None
    addresses = dict()
    history = []

    def name(self, address):
        return self.addresses.get(address, address[:4])

    def format_debug(self, data):
        def is_printable(str):
            return set(str).issubset(string.printable)

        try:
            d = ''.join(chr(x) for x in data['result'])
        except TypeError as e:
            print e
            print data
            return
        o = serpent.decode_datalist(d)
        words =  map(lambda x: x-2**256 if x > 2**255 else x, o)
        if words and words[0] == 0xdeba6:
            self.debug_contract = data['to']
            self.register_address('debug', data['to'])
            if len(words) < 2:
                print "DEBUG:\t%r > %r" %  (self.name(data['sender']), [])
                return
            h = hex(words[1])[2:].replace('L','')
            try:
                label = ('0' + h if len(h) % 2 else h).decode('hex')
            except TypeError:
                label = '0x%s' % h
            if is_printable(label):
                print "DEBUG:\t%r > %r: %r" % (self.name(data['sender']).ljust(4), label, words[2:])
            else:
                print "DEBUG:\t%r > %r" %  (self.name(data['sender']), words[1:])
            return True

    def format_msg(self, data, label='MSG'):
        if data['to'] != self.debug_contract:
            sender = self.name(data.get('sender', '')).ljust(4)
            to = self.name(data.get('to', ''))
            print '%s:\t%r > %r: v:%r gas:%r' %(label, sender, to, data['value'], data['gas'])

    def format_tx(self, data):
        data['gas'] = data['startgas']
        self.format_msg(data, label="TX")

    def message_failed(self, data):
        data['gas'] = 'remained:%r' % data['gas_remained']
        #data['sender'] = ''
        data['value'] = ''
        self.format_msg(data, label="FAILED")

    def log_receiver(self, name, data):
        self.history.append((name, data))
        if name == 'MSG APPLIED':
            if data['result'] == -1:
                self.message_failed(data)
            else:
                self.format_debug(data)
        elif name == 'TX NEW':
            self.format_tx(data['tx_dict'])
        elif name == 'MSG APPLY':
            self.format_msg(data)
        else:
            pass

    def register_address(self, name, address):
        self.addresses[address] = name

    def get_history(self, num=1):
        return self.history[-num:]

    def print_log_history(self, num):
        print '\n'.join(repr(x) for x in self.get_history(num))


logger = Logger()

pyethereum.processblock.pblogger.listeners.append(logger.log_receiver)
pyethereum.processblock.pblogger.log_post_state = True
pyethereum.processblock.pblogger.log_op = False


#  gas limit is what is sent as tx gas
# gas_price = 1
pyethereum.tester.gas_limit = 10**5 - 10**4

def run(code, value=0, data=[]):
    if os.path.exists(code):
        print "reading from file", code
        code = open(code).read()
    s = tester.state()
    c = s.contract(code, sender=tester.k0)
    return s.send(tester.k0, c, value, data)
