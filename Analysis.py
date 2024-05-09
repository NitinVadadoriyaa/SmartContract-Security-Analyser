import sys
sys.path.append('/home/nitin/Desktop/Tool/')
import variable

#TODO Vulnrable part
VulnrablePartDict = {} # vulnarability name ==> [keywords]

#-------------------------------------------------Private Data Read-----------------------------------------------------#
#-----scaning statevariable first-----#
stateVariables = variable.stateVariable()

variableDict = {} #---Making key-value pair : searching become fast---#
for var in stateVariables:
    variableDict[var.varName] = var

for var in stateVariables:
    if var.visibility == "private":
        print("     ||---------------------------------------------------------------------------------------------||")
        print("     || Private Data Read.     || " + var.varName)
        print("     ||---------------------------------------------------------------------------------------------||")

    elif var.operator == "+" and var.dataType[0] == 'u':
        if var.funcName != "None":
            print("     ||---------------------------------------------------------------------------------------------||")
            print("     || Integer Overflow.     || " + var.varName + " || " + " || + || ")
            print("     ||---------------------------------------------------------------------------------------------||")



#-------------------------------------------------Overflow & Underflow-----------------------------------------------------#
#-----Looking every methods and analysis------#
import method
allMethods,functionExpression,functionLocalVariable,AllConditionStatment = method.method_Information()

functionLocalVariableDict = {} #---Making key-value pair : searching become fast---#
for key in functionLocalVariable:
        if len(functionLocalVariable[key]) != 0: #functionName --> array of local var
            for exp in functionLocalVariable[key]:
                functionLocalVariableDict[exp.varName] = exp

for method in allMethods: #---parameter local variable---#
        if len(method.parameterList) != 0:
            for par in method.parameterList:
                functionLocalVariableDict[par.varName] = par

for key in functionExpression:
        for exp in functionExpression[key]:
    
            if exp.type == "BinaryOperation" and (exp.operator == "+=" or exp.operator == "*="):
                if ((exp.left.baseName in variableDict) or (exp.left.baseName in functionLocalVariableDict)) and ((exp.right.baseName in variableDict) or (exp.right.baseName in functionLocalVariableDict)):#TODO CONSIDER A = A + 100 [constant]
                                                                                                                                                                                                            #TODO CONSIDER UNIORYOPERATOR ++ / --
                   print("     ||---------------------------------------------------------------------------------------------||")
                   print("     || Integer Overflow.     || " + exp.left.baseName + " || " + exp.operator  + " || ")
                   print("     ||---------------------------------------------------------------------------------------------||")

            if exp.type == "BinaryOperation" and (exp.operator == "-="):
                if ((exp.left.baseName in variableDict) or (exp.left.baseName in functionLocalVariableDict)) and ((exp.right.baseName in variableDict) or (exp.right.baseName in functionLocalVariableDict)):#TODO CONSIDER A = A - 100 [constant]

                    print("     ||---------------------------------------------------------------------------------------------||")
                    print("     || Integer Underflow.     || " + exp.left.baseName +  " || " + exp.operator  + " || ")
                    print("     ||---------------------------------------------------------------------------------------------||")

                

#-------------------------------------------------Block Time Manipulation-----------------------------------------------------#
#1. check any locak & state variable depend on BlockTime
#2. check that variable used in any conditional statment
blockDependedVar = {}

for var in stateVariables: #data dependency on state variable
    if var.baseName == "block" or var.parentMember == "block":
        blockDependedVar[var.varName] = True

for var in stateVariables: #data dependency on state variable
     if var.left in blockDependedVar or var.right in blockDependedVar:
          blockDependedVar[var.varName] = True

def check_0(varDetail): #helper method
    res1 = (varDetail.baseName == "block" or varDetail.parentMember == "block" or varDetail.childMember == "block")
    
    return res1

def check_1(varDetail): #helper method
    res2 = False
    res3 = False
    if varDetail.left != "None":
        res2 = varDetail.left.baseName == "block" or varDetail.left.parentMember == "block" or varDetail.left.childMember == "block"
    if varDetail.right != "None":
        res3 = varDetail.right.baseName == "block" or varDetail.right.parentMember == "block" or varDetail.right.childMember == "block"
    
    return res2 or res3

def check_2(varDetail): #helper method
    res2 = False
    res3 = False
    if varDetail.left != "None":
        res2 = (varDetail.left.baseName in functionLocalVariableDict) or (varDetail.left.parentMember in functionLocalVariableDict) or (varDetail.left.childMember in functionLocalVariableDict)
    if varDetail.right != "None":
        res3 = (varDetail.right.baseName in functionLocalVariableDict) or (varDetail.right.parentMember in functionLocalVariableDict) or (varDetail.right.childMember in functionLocalVariableDict)
        
    return res2 or res3

for var in functionLocalVariableDict: #data dependency on local variable
    if "baseName" in var:
        if (check_0(functionLocalVariableDict[var])):
            blockDependedVar[var] = True

for key in functionExpression: #data dependency in local expression
    for exp in functionExpression[key]:
         if (check_2(exp) or check_1(exp)):
            blockDependedVar[exp.left.baseName] = True

for con in AllConditionStatment:
     left = con.left.baseName #varName
     right = con.right.baseName #varName
     if left in blockDependedVar:
          print("     ||---------------------------------------------------------------------------------------------||")
          print("     || BlockTimeManipuleted.     || " + left + " || ")
          print("     ||---------------------------------------------------------------------------------------------||")
     elif right in blockDependedVar:
          print("     ||---------------------------------------------------------------------------------------------||")
          print("     || BlockTimeManipuleted.     || " + right + " || ")
          print("     ||---------------------------------------------------------------------------------------------||")

              

#------------------------------------Deninal of service----------------------------------------------#
#function must be external
#function send token to caller
for method in allMethods:
    if method.visibility == "external":
        #TODO : YOU HAVE TO JUST IDENTIFY SENDER METHOD INVOLE IN CURRENT METHOD OR NOT
        for exp in functionExpression[method.funcName]:
            
            if exp.left.type == "transfer" and exp.left.childMember == "sender":
                print("     ||---------------------------------------------------------------------------------------------||")
                print("     || Denial Of Service.     || " + method.funcName + "() || ")
                print("     ||---------------------------------------------------------------------------------------------||")

        #For Data-Dependency
            elif exp.left.type == "transfer" and exp.left.childMember != "None":
                for exp in functionLocalVariable[method.funcName]:
                    if exp.parentMember == "msg" and exp.childMember == "sender": #TODO: check-recursivly && also check for state-variable
                        print("     ||---------------------------------------------------------------------------------------------||")
                        print("     || Denial Of Service.     || " + method.funcName + "() || ")
                        print("     ||---------------------------------------------------------------------------------------------||")
               
        