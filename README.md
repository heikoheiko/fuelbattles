FUEL BATTLES
============
-- *AI challenge on the blockchain*

Fuel Battles is a grid based AI challenge designed for Ethereum - a generalized, decentralized consensus platform. Ethereum features the concept of autonomous contracts which are accounts with associated code, living on the blockchain. In Ethereum code is executed whenever a transaction is sent to a contract. In order to cope with the halting problem, there is the concept of gas. Gas is needed to fuel code execution and has to be bought at the current gas price (in the blockchain) in exchange for Ether, the internal currency of Ethereum.

Fuel Battles is a challenge which mirrors the '*computation comes at a cost*' aspect of Ethereum. It requires to create good AI implementations that balance the utilization of gas (computing power) with the complexity of an AI strategy.

Game Mechanics
--------------

The game takes place on a NxM grid and is about amounting 'fuel', which can be accumulated by occupying cells on the grid. But calculating the next turn also costs fuel. 

The fuel in the game is initially equal the gas provided by the calling transaction. It is reduced each turn by the amount of gas necessary to compute the next step. 

The game is synchronous turn based (i.e. each player has to decide on the next turn without knowing the next move of the opponent).  Each player starts with the same amount of fuel which is initially placed on a pseudo randomly selected cell within the grid. 

Fuel at a cell can (partially) be moved to the 4 neighbour cells (left, up, right, down). Each cell provides some fuel per turn, which is a certain fraction of the total fuel in the system (which is the sum of both players fuel) . Players seek to conquer cells that provide a high fraction of fuel distributed per turn. The provided fuel in each turn is deducted from the player as a fraction of the sum of the fuel on the cells they have placed fuel at. 

Each turn the fuel of the players is individually reduced by the gas it took to compute their next move and for both by half of the the gas that was used to verify the moves and update the stage. 

If a player moves fuel to a cell that is already taken by the opponent, the difference is destroyed (and redistributed) and the player with the higher amount of fuel has the remaining fuel placed on the cell. 

The winner is defined as the player with some fuel left once one player runs out of fuel. Both initially placed stakes are transfered by the organizing contract  to the winning party.


