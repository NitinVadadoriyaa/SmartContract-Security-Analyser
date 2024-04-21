// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

/*
Roulette is a game where you can win all of the Ether in the contract
if you can submit a transaction at a specific timing.
A player needs to send 10 Ether and wins if the block.timestamp % 15 == 0.
*/

/*
1. Deploy Roulette with 10 Ether
2. Eve runs a powerful miner that can manipulate the block timestamp.
3. Eve sets the block.timestamp to a number in the future that is divisible by
   15 and finds the target block hash.
   Miner have liberty to choce block.timestamp with in some rang..
   Normal user not have this power....
4. Eve's block is successfully included into the chain, Eve wins the
   Roulette game.
*/

contract Roulette {
    uint256 public pastBlockTime;
    address winner;
 
    uint tim = block.timestamp;
   uint public tim2 = 10 * tim;

    constructor() payable {}

    function spin() external payable {
        require(msg.value == 10 ether); // must send 10 ether to play
        require(block.timestamp != pastBlockTime); // only 1 transaction per block

        pastBlockTime = block.timestamp;
        uint bt1;
        uint bt = block.timestamp % 15;
        bt1 = 100 * bt;
        if (bt == 0) {
            winner = msg.sender;
        }
    }

    function climReward() external {
        require(msg.sender == winner, "You are not winner");
        payable(msg.sender).transfer(address(this).balance);
    }
}