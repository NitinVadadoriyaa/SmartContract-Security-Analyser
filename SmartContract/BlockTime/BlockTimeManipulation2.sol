// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/*
NOTE: cannot use blockhash in Remix so use ganache-cli

npm i -g ganache-cli
ganache-cli
In remix switch environment to Web3 provider
*/

/*
GuessTheRandomNumber is a game where you win 1 Ether if you can guess the
pseudo random number generated from block hash and timestamp.

At first glance, it seems impossible to guess the correct number.
But let's see how easy it is win.

1. Alice deploys GuessTheRandomNumber with 1 Ether
2. Eve deploys Attack
3. Eve calls Attack.attack() and wins 1 Ether

What happened?
Attack computed the correct answer by simply copying the code that computes the random number.
*/

contract GuessTheRandomNumber {
    constructor() payable {}

    function guess(uint256 _guess) public {
        uint256 answer = block.timestamp + block.number;
        answer = answer * 555;
        answer = answer % 1000;

        if (_guess == answer) {
            payable(msg.sender).transfer(1 ether);
        }
    }
}