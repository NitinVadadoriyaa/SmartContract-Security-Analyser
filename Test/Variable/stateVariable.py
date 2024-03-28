import sys
sys.path.append('/home/nitin/Desktop/Tool/')
import variable

stateVariables = variable.stateVariable()

variableDict = {}
for var in stateVariables:
    variableDict[var.varName] = var

for var in stateVariables:
    if var.visibility == "private":
        print()
        print("Private Data Read.")
    elif var.operator == "+" and var.dataType[0] == 'u':
        if var.funcName != "None":
            print() 
            print("Integer Overflow.")

