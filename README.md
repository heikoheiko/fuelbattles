FUEL BATTLES
============
-- *AI challenge on the blockchain*

Fuel Battles is a grid based simulation and AI challenge designed for [Ethereum](https://github.com/ethereum/wiki/wiki) - a generalized, decentralized consensus platform.

It is inspired by the conquest game [Galcon](https://en.wikipedia.org/wiki/Galcon), with cells on a grid emulating the planets and fuel instead of space ships, minus graphics.

The software implements an environment in which AIs can compete within the blockchain.

Ethereum features the concept of autonomous contracts which are accounts with associated code, living on the blockchain. In Ethereum code is executed whenever a transaction is sent to a contract. In order to cope with the [halting problem](https://en.wikipedia.org/wiki/Halting_problem), there is the concept of gas. Gas is needed to fuel code execution and has to be converted at the current gas price (of the current block) in exchange for Ether, the internal currency of Ethereum.

Fuel Battles mirrors the *computation comes at a cost* aspect of Ethereum. It requires to create good AI implementations that balance the utilization of gas (computing power) with the complexity of an AI strategy.


Playing the Game
----------------

Install Python2.7 and the necessary libraries
> git clone https://github.com/heikoheiko/fuelbattles/

> cd fuelbattles

> pip install -r requirements.txt

The [serpent](https://github.com/ethereum/wiki/wiki/Serpent) (Ethereum HLL) version can be run in a local (offline) test environment:
> cd serpent

> python runsim.py

There is also a pure Python based prototype which can be run with
> python python/run.py


Out of the box the software runs a local simulation with two predefined AIs competing about resources on a pseudo randomly generated grid.

Actually _playing the game_, involves the development (coding) of an AI contract and let it compete with other AIs on the Ethereum blockchain.


Game Mechanics
--------------

```
B61| B27| B10| B18| B14| B 6|
-----------------------------
B74| B14| B18| B 9| B34| B10|
-----------------------------
B55|      B 5| A 4| A99| A80|
-----------------------------
B28| B51| B13| A11|      B18|
-----------------------------
B20| B61| B25| B 9| B 7| B31|
-----------------------------
B17| B33| B22| B 9| B18| B30|
----------------------------
```
*The Stage: A 6x6 grid, displaying the amount of fuel the AIs (A,B) have at each cell*

The game takes place on a NxM grid and is about amounting *fuel*, which can be accumulated by occupying cells on the grid. But calculating the next turn also costs *gas*, which reduces a players fuel supplies.

In the following `fuel` refers to the amount the players have at cells in grid and which they are competing for. The term `gas` refers to the internal currency of the EVM (Ethereum Virtual Machine) which has to be provided at every computing step. Both are interlinked as the gas required to compute the next move by the AI is deducted from the players fuel on the grid.

The game is started once two externally owned accounts (i.e. users) have sent a transaction to the organizer (contract), each with a stake and the address of the AI contract which shall calculate the move at each turn.

The fuel in the game is initially equal the gas provided by the calling transaction. It is reduced each turn by the amount of gas necessary to compute the next step. At the end of each turn the fuel in the game is equal to the gas which is available the executing contract and needed to be further executed by the EVM (Ethereum Virtual Machine).

Each player starts with the same amount of fuel which is initially placed on a pseudo randomly selected cell within the grid.

At each turn the AIs decide on a move.  This is the transfer of fuel from a selected cell to one of its 4 neighbour cells (left, up, right, down).

Each cell is a source of fuel to the occupier, with the amount being a certain fraction of the total fuel in the system (the sum of both players fuel). Different cells provide different amount of fuel. Players seek to conquer cells that provide a high fraction of fuel distributed per turn. The provided fuel in each turn is deducted from the players as a fraction of the sum of the fuel on the cells they have placed fuel at. The player which is on lower fuel yielding cells, looses more fuel per turn.

Each turn the fuel of the players is individually reduced by the gas it took to compute their next move and for both by half of the the gas that was used to verify the moves and update the stage.

If a player moves fuel to a cell that is already taken by the opponent, the difference is destroyed (and redistributed) and the player with the higher amount of fuel has the remaining fuel placed on the cell.

The winner is defined as the player with the most fuel left, once either the other player runs out of fuel or the simulation would run out of gas in the next turn. The balance of the organizer contract (both initially placed stakes minus the gas_cost) are transfered to the winning party.

The game is synchronous turn based, i.e. each player has to decide on the next turn without knowing the next move of the opponent.

Game Logic
----------

**Setting up the battle**

    Player A sends a transaction to the organizer with
        - a stake (Ether value sent to the organizer)
        - address of the AI contract to be executed when calculating moves of A
        - value of the minimal amount of gas required to accept the challenge
    Player B sends a transaction to the organizer with
        - a stake matching the stake sent by A
        - address of the AI contract to be executed when calculating moves of B
        - gas matching the target set by A

    The Organizer
        - if receiving the 1st transaction
            - the value sent is added to organizers balance (escrow)
            - the AI address and gas requirement are stored
        - if receiving the 2nd transaction
            - the value sent is added to organizers balance (escrow)
            - if the the gas requirement or the stake is not matched
                - refund both parties
                - reset storage
                - exit
            - the simulation is called with all gas and the two AI addresses
            - once the simulation stops and returns the winning AI address
                - refund the gas cost to account of player b
                - transfer the remaining balance to the account of the player with the winning AI
                - reset storage

**Running the battle**

    The Simulation
        - set up a NxM grid
        - with a pseudo random number as the seed
            - set up a NxM central point symetric redistribution grid
              i.e. weigths at cells which represent the fuel redistribution factor
            - select the two cell that players have their fuel placed at initially
              both players are positioned on central point mirrored cells
        - while player A and player B have fuel and the simulation has sufficient gas
            - get move A by calling the AI contract of player A with the grids
            - get move B by calling the AI contract of player B with the grids
            - with both players and their moves [from, to, fuel]
                - if the move is valid, which it is if
                  from and to cells are neighbours
                  to be moved amount of fuel is available at from cell
                    - move specified fuel on grid from > to
                - subtract
                  the gas_used by the AI to calculate the move
                  and the half of the gas used for the last simulation step
                  proportionally from each cell occupied by the player, based on its fuel
            - calculate the amount of fuel to be redistributed
              redist_allowance = total fuel on grid redist_factor
            - subtract the redist_allowance from each occupied cell
              proportionally to the fuel at cell
            - with each collision which is when
              fuel is moved to a cell which is occupied by the opponent
                - subtract the fuel difference from both players at the cell
                  leaving one with player with no fuel on the cell
                - add the difference to the redist_allowance
            - distribute the redist_allowance
              for the occupied cells
              - redistribution is proportionally to the cell weight in the redistribution grid
              - add the redistribution to the cell
            - record the gas used for the simulation step




Writing your own Fuel Battles AI
--------------------

Fuel Battles as it is, basically sets the stage for trust free grid battles on the blockchain, by implementing the organizer and simulator contracts.
While it comes with two AI implementations, these are very limited and serve as examples.

Check `serpent/runsim.py` and `serpent/ai_simple.se` to see how AIs are implemented and invoked.


Notes
-----

The complete simulation has to be run in one transaction in one block. Therefore the simulation time is limited by the `block.gas_limit`. In effect only small grids and not too complex AIs are currently feasible. Once the `ALARM` feature becomes available in Ethereum (PoC7), the simulation steps can be distributed over multiple blocks and the gas cost probably be supplied by the organizer contract. This is when more complex AI strategies can be run on the Ethereum blockchain. These limitations can be circumvented when running in the local test environment.

The current implementation has an opinionated approach which prefers convenience over efficiency, when calling the AIs. It basically sends the whole state of the simulation, rather then sending only the starting parameters (grid dimensions, seed, etc.) in the first call and no more than the opponents move in successive calls.
The implementation is neither optimized for CPU nor memory efficiency yet. These would come at the cost of simplicity and code readability, but might be worthwhile in the future to have more gas available to the AIs.


Is this somehow useful?
-----------------------

The current implementation was written as a first exercise in writing contracts for Ethereum and is still limited.

In the future it could be extended to serve as a trust free environment in which confident developers would enter a trial of strength and place bets on their AI implementations.


