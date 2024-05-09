// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Bank {
 uint private  x = 10;
    mapping (address => uint256) accounts;

    function withdraw(uint _value) external payable {
        require(accounts[msg.sender] >= _value, "You can not withdraw more then you hold!");
        address winner;
        payable (msg.sender).transfer(_value);

        accounts[msg.sender] -= _value;
    }

    function deposit() external payable {
        
        accounts[msg.sender] += msg.value;
    }
}

// contract Attack {
//     Bank bank;

//     constructor(Bank _bank) {
//         bank = Bank(_bank);
//     }

//     function attack(uint _value) public payable {
//         bank.withdraw(_value); // sending ether to other smart contract
//     }

//     function deposit() public payable  {
//         bank.deposit{value : msg.value}();
//     }
   
// }