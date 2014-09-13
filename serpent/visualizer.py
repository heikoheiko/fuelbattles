"""
THIS IS A HACK
"""
import sys
import string
import pyethereum
import serpent
import testenv
sys.path.append('../python/')
import ui



def format_debug(self, data):
    try:
        d = ''.join(chr(x) for x in data['result'])
    except TypeError as e:
        return
    o = serpent.decode_datalist(d)
    words =  map(lambda x: x-2**256 if x > 2**255 else x, o)
    if words and words[0] == 0xdeba6:
        if len(words) >= 4 + 4 * 16 + 1: # have at least 16 cells
            words = words[1:]
            #msg.data = [cols, rows, a_ai, b_ai] + [a_grid] + [b_grid] + [sorted_redistribution_grid]
            ncells = words[0] * words[1]

            # restore redist
            redist = [0] * ncells
            for i in range(ncells):
                v = words[4 + ncells * 2 + i*2]
                c = words[4 + ncells * 2 + i*2 + 1]
                redist[c] = v

            ui.draw(sim_steps=0, cols=words[0], rows=words[1], a_grid=words[4:4+ncells],
                b_grid=words[4+ncells:4+ncells*2], redistribution_grid=redist)

def log_receiver(self, name, data):
    if name == 'MSG APPLIED':
        if data['result'] != -1:
            self.format_debug(data)

testenv.Logger.log_receiver = log_receiver
testenv.Logger.format_debug = format_debug
testenv.logger = testenv.Logger()

pyethereum.processblock.pblogger.listeners = [testenv.logger.log_receiver]