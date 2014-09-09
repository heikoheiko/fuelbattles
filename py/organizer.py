from simulator import call as call_simulator
gas_price = 1

storage = [0]

def call(sender, value, ai):
    if storage[0] < 2:
        storage.extend([sender, value, ai])
        storage[0] += 1
    if storage[0] == 2:
        if storage[2] != storage[5]:
            # refund & reset
            storage[1:7] = []
            storage[0] = 0
            return

        # provide gas
        gas = (storage[2] + storage[5]) / gas_price
        # call simulation
        gas_used, winner = call_simulator(storage[1], storage[4], storage[3], storage[6], gas)

        # reconvert_gas
        reward = (gas-gas_used)*gas_price
        investment = gas*gas_price/2
        print 'Winner:%r reward%d investment:%d return:%r' %(winner, reward, investment, reward/float(investment))
