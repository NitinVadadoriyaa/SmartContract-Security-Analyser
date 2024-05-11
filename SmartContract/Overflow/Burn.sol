pragma solidity 0.6.4;
// This is a simplified example of a token contract with custom checks
contract Token {
    uint public totalSupply;
    uint public constant MAX_SUPPLY = 1000000;

    function mint(uint amount) public {
        // This will cap the totalSupply at MAX_SUPPLY if totalSupply + amount exceeds it
        require(totalSupply + amount <= MAX_SUPPLY);
            totalSupply += amount;
    }
    function burn(uint amount) public {
        // This will set the totalSupply to zero if totalSupply - amount is negative
       require(totalSupply - amount >= 0);
            totalSupply -= amount;   
    }
}        