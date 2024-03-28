pragma solidity 0.8.25;

contract ChangeBalance {
    uint8 public balance;

    function decrease() public {
        balance--;
    }

    function increase() public {
        balance++;
    }
}
