import Ast_Generator

def start_analysis(fileName):
    Ast_Generator.generate_ast(fileName)

    # print(jsonObject)

    #---- make file for store enviromental variable ----#
    with open("env.py", 'w') as f:
        f.write(f'fileName = "{fileName}"\n')

    import Analysis
    Analysis.doAnalysis()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <fileName.sol>")
        sys.exit(1)
    
    fileName = sys.argv[1]
    start_analysis(fileName)