import json
import os.path
from solidity_parser import parser

def generate_ast(fileName):
    # Parse Solidity code into AST
    sourceUnit = parser.parse_file(fileName, loc=False)  # loc=True -> add location information to ast nodes

    # Stor AST in JSON format
    fileName_without_extension = os.path.splitext(fileName)[0]
    with open(f"{fileName_without_extension}_ast.json", "w") as f:
        json.dump(sourceUnit, f, indent=2)


    print("successfuly : AST generated and stored in", f"{fileName_without_extension}_ast.json")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python Ast_Generator.py <fileName>")
        sys.exit(1)
    
    fileName = sys.argv[1]
    generate_ast(fileName)
