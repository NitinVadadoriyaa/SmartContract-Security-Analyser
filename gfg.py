from solidity_parser import parser

# Solidity code snippet
solidity_code = """
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
"""

# Parse Solidity code into AST
ast = parser.parse(solidity_code)

# Print AST in JSON format
import json
print(json.dumps(ast, indent=2))

