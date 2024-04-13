import sys
sys.path.append('/home/nitin/Desktop/Tool/')
import variable

#-----scaning statevariable first-----#
stateVariables = variable.stateVariable()

variableDict = {} #---Making key-value pair : searching become fast---#
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

#-----Looking every methods and analysis------#
import method
allMethods,functionExpression,functionLocalVariable = method.method_Information()

functionLocalVariableDict = {} #---Making key-value pair : searching become fast---#
for key in functionLocalVariable:
        for exp in functionLocalVariable[key]:
            functionLocalVariableDict[exp.varName] = exp

for method in allMethods: #---parameter local variable---#
        if len(method.parameterList) != 0:
            for par in method.parameterList:
                functionLocalVariableDict[par.varName] = par

# for method in allMethods:
#         print(method.funcName)
#         if len(method.parameterList) != 0:
#             for par in method.parameterList:
#                 print(par.type)
#                 print(par.dataType)
#                 print(par.varName)
#                 print(par.storageLocation)
#                 print(par.isStateVar)
#                 print()
#         if len(method.returnParameterList) != 0:
#             par = method.returnParameterList[0]
#             print(par.type)
#             print(par.dataType)
#             print(par.varName)
#             print(par.storageLocation)
#             print(par.isStateVar)
#             print()

for key in functionExpression:
        # print("Method Name : " + key) 
        for exp in functionExpression[key]:
            # print(exp.type)
            # print(exp.operator)
            # print(exp.left.type)
            # print(exp.left.value)
            # print(exp.left.baseName)#varName
            # print(exp.left.indexType)
            # print(exp.left.parentMember)
            # print(exp.left.childMember)
            # print(exp.right.type)
            # print(exp.right.value)
            # print(exp.right.baseName)#varName
            # print(exp.right.indexType)
            # print(exp.right.parentMember)
            # print(exp.right.childMember)
            # print()
            if exp.type == "BinaryOperation" and (exp.operator == "+=" or exp.operator == "*="):
                if ((exp.left.baseName in variableDict) or (exp.left.baseName in functionLocalVariableDict)) and ((exp.right.baseName in variableDict) or (exp.right.baseName in functionLocalVariableDict)):#TODO CONSIDER A = A + 100 [constant]
                                                                                                                                                                                                            #TODO CONSIDER UNIORYOPERATOR ++ / --
                    print()
                    print("Integer Overflow.")
            if exp.type == "BinaryOperation" and (exp.operator == "-="):
                if ((exp.left.baseName in variableDict) or (exp.left.baseName in functionLocalVariableDict)) and ((exp.right.baseName in variableDict) or (exp.right.baseName in functionLocalVariableDict)):#TODO CONSIDER A = A - 100 [constant]
                    print()
                    print("Integer Underflow.")
                
# for key in functionLocalVariable:
#         print(key)
#         for exp in functionLocalVariable[key]:
#             print(exp.dataType)
#             print(exp.varName)
#             print(exp.storageLoc)
#             print(exp.value)
#             print(exp.intializeType)
#             print(exp.parentMember)
#             print(exp.childMember)
#             print(exp.baseName)
#             print(exp.indexType)
#             print(exp.operator)
#             if exp.left != "None":
#                 print(exp.left.type)
#                 print(exp.left.value)
#                 print(exp.left.baseName)#varName
#                 print(exp.left.indexType)
#                 print(exp.left.parentMember)
#                 print(exp.left.childMember)
#             if exp.right != "None":
#                 print(exp.right.type)
#                 print(exp.right.value)
#                 print(exp.right.baseName)#varName
#                 print(exp.right.indexType)
#                 print(exp.right.parentMember)
#                 print(exp.right.childMember)
#             print()