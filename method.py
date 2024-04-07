
def method_Information():
    import env
    import build_json
    from enum import Enum

    fileName = env.fileName
    jsonFileName = fileName.rsplit('.',1)[0] + "_ast.json"
    jsonObject = build_json.build_json(jsonFileName)
    # print(jsonObject)

    methods = jsonObject["children"][1]["subNodes"]

    #----------Method.Parameter-----------------#
    class Parameter:
        def __init__(self,type,dataType,varName,storageLocation,isStateVar):
            self.type = type
            self.dataType = dataType
            self.varName = varName#variable name
            self.storageLocation = storageLocation
            self.isStateVar = isStateVar

    class Method:
        def __init__(self,funcName,visibility,isConstructor,isFallback,isReceive,stateMutability = "None",parameterList = [],returnParameterList=[]):
            self.funcName = funcName
            self.visibility = visibility
            self.isConstructor = isConstructor
            self.isFallback = isFallback
            self.isReceive = isReceive
            self.stateMutability = stateMutability
            self.parameterList = parameterList
            self.returnParameterList = returnParameterList

    allMethods = []

    #----------Expression.Operator-----------------#

    class Operator:
        def __init__(self,type,value,baseName,indexType,parentMember,childMember):
            self.type = type
            self.value = value
            self.baseName = baseName #varName
            self.indexType = indexType
            self.parentMember = parentMember
            self.childMember = childMember
            
    class Expression:
        def __init__(self,type,operator,left,right):
            self.type = type
            self.operator = operator
            self.left = left
            self.right = right

    #----------{functionName : Array Of Expression-----------------#
    functionExpression = {} 

    class LocalVariable:
        def __init__(self,dataType,varName,storageLoc,value,intializeType,parentMember,childMember,baseName,indexType,operator,left,right):
            self.dataType = dataType
            self.varName = varName#variable name
            self.storageLoc = storageLoc
            self.value = value
            self.intializeType = intializeType
            self.parentMember = parentMember
            self.childMember = childMember
            self.baseName = baseName
            self.indexType = indexType
            self.operator = operator
            self.left = left
            self.right = right

    #----------{functionName : Array Of LocalVariable-----------------#
    functionLocalVariable = {}

    for key in methods:
        if key["type"] == "FunctionDefinition":
            funcName = key["name"]
            visibility = key["visibility"]
            isConstructor = key["isConstructor"]
            isFallback = key["isFallback"]
            isReceive = key["isReceive"]
            parameterList = []
            returnParameterList = []
            if  key["stateMutability"] != "null":
                stateMutability = key["stateMutability"]

            if len(key["parameters"]["parameters"]) != 0: #--- input parameters ---#
                for obj in key["parameters"]["parameters"]:
                    parameterList.append(Parameter(obj["typeName"]["type"],obj["typeName"]["name"],obj["name"],obj["storageLocation"],obj["isStateVar"]))

            if len(key["returnParameters"]) != 0: #--- return parameters ---#
                obj = key["returnParameters"]["parameters"][0]
                returnParameterList.append(Parameter(obj["typeName"]["type"],obj["typeName"]["name"],obj["name"],obj["storageLocation"],obj["isStateVar"]))
            
            allMethods.append(Method(funcName,visibility,isConstructor,isFallback,isReceive,stateMutability,parameterList,returnParameterList))
            
            allExpression = []
            allLocalVariable = []

            if len(key["body"]["statements"]) != 0: #------All Expression of individual function------#
                statements = key["body"]["statements"]
                for obj in statements:
                    expType = "None"
                    expOperator = "None"
                    expLeft = "None"
                    expRight = "None"
                    
                    if obj["type"] == "ExpressionStatement":#--------Only Expression--------#
                        obj = obj["expression"]
                        expType = obj["type"]
                        if expType == "BinaryOperation": #----Only binary operation----#

                            expOperator = obj["operator"]

                            #----- LEFT --------#
                            type = "None"
                            value = "None"
                            baseName = "None"
                            indexType = "None"
                            parentMember = "None"
                            childMember = "None"

                            type = obj["left"]["type"]
                            if type == "IndexAccess":
                                baseName = obj["left"]["base"]["name"]
                                indexType = obj["left"]["index"]["type"]

                                if indexType == "MemberAccess":
                                    parentMember = obj["left"]["index"]["expression"]["name"]
                                    childMember = obj["left"]["index"]["memberName"]
                                elif indexType == "NumberLiteral":
                                    value = obj["left"]["number"]
                            
                            elif type == "MemberAccess":
                                parentMember = obj["left"]["expression"]["name"]
                                childMember = obj["left"]["memberName"]

                            elif type == "Identifier":
                                baseName = obj["left"]["name"]

                            elif type == "NumberLiteral":
                                value = obj["left"]["number"]

                            elif type == "BooleanLiteral":
                                value = obj["left"]["value"]

                            expLeft = Operator(type,value,baseName,indexType,parentMember,childMember)

                            #--------RIGHT-------#
                            type = "None"
                            value = "None"
                            baseName = "None"
                            indexType = "None"
                            parentMember = "None"
                            childMember = "None"

                            type = obj["right"]["type"]
                            if type == "IndexAccess":
                                baseName = obj["right"]["base"]["name"]
                                indexType = obj["right"]["index"]["type"]

                                if indexType == "MemberAccess":
                                    parentMember = obj["right"]["index"]["expression"]["name"]
                                    childMember = obj["right"]["index"]["memberName"]
                                elif indexType == "NumberLiteral":
                                    value = obj["right"]["number"]
                            
                            elif type == "MemberAccess":
                                parentMember = obj["right"]["expression"]["name"]
                                childMember = obj["right"]["memberName"]

                            elif type == "Identifier":
                                baseName = obj["right"]["name"]

                            elif type == "NumberLiteral":
                                value = obj["right"]["number"]

                            elif type == "BooleanLiteral":
                                value = obj["right"]["value"]

                            expRight = Operator(type,value,baseName,indexType,parentMember,childMember)

                            allExpression.append(Expression(expType,expOperator,expLeft,expRight))

                    elif obj["type"] == "VariableDeclarationStatement":#--------Only Local Variable--------#
                        dataType = "None"
                        varName = "None"
                        storageLoc = "None"
                        value = "None"
                        intializeType = "None"
                        parentMember = "None"
                        childMember = "None"
                        baseName = "None"
                        indexType = "None"
                        operator = "None"
                        left = "None"
                        right = "None"

                        obj1 = obj["variables"][0]
                        dataType = obj1["typeName"]["name"]
                        varName = obj1["name"]
                        storageLoc = obj1["storageLocation"]
                        if obj["initialValue"] != None: #-----------in ast null == None in python-----------#
                            obj1 = obj["initialValue"]
                            intializeType = obj1["type"]
                            
                            if intializeType == "MemberAccess":
                                parentMember = obj1["expression"]["name"]
                                childMember = obj1["memberName"]

                            elif intializeType == "IndexAccess":
                                baseName = obj1["base"]["name"]
                                indexType = obj1["index"]["type"]
                                if indexType == "MemberAccess":
                                    parentMember = obj1["index"]["expression"]["name"]
                                    childMember = obj1["index"]["memberName"]    

                            elif intializeType == "Identifier":
                                value = obj1["name"]

                            elif intializeType == "BooleanLiteral":
                                value = "False" if obj1["value"] == "false" else "true"
                            
                            elif intializeType == "NumberLiteral":
                                value = obj1["number"]

                            elif intializeType == "BinaryOperation":
                                operator = obj1["operator"]
                                obj = obj1

                                #----- LEFT --------#
                                type = "None"
                                value = "None"
                                baseName = "None"
                                indexType = "None"
                                parentMember = "None"
                                childMember = "None"

                                type = obj["left"]["type"]
                                if type == "IndexAccess":
                                    baseName = obj["left"]["base"]["name"]
                                    indexType = obj["left"]["index"]["type"]

                                    if indexType == "MemberAccess":
                                        parentMember = obj["left"]["index"]["expression"]["name"]
                                        childMember = obj["left"]["index"]["memberName"]
                                    elif indexType == "NumberLiteral":
                                        value = obj["left"]["number"]
                                
                                elif type == "MemberAccess":
                                    parentMember = obj["left"]["expression"]["name"]
                                    childMember = obj["left"]["memberName"]

                                elif type == "Identifier":
                                    baseName = obj["left"]["name"]

                                elif type == "NumberLiteral":
                                    value = obj["left"]["number"]

                                elif type == "BooleanLiteral":
                                    value = obj["left"]["value"]

                                left = Operator(type,value,baseName,indexType,parentMember,childMember)

                                #--------RIGHT-------#
                                type = "None"
                                value = "None"
                                baseName = "None"
                                indexType = "None"
                                parentMember = "None"
                                childMember = "None"

                                type = obj["right"]["type"]
                                if type == "IndexAccess":
                                    baseName = obj["right"]["base"]["name"]
                                    indexType = obj["right"]["index"]["type"]

                                    if indexType == "MemberAccess":
                                        parentMember = obj["right"]["index"]["expression"]["name"]
                                        childMember = obj["right"]["index"]["memberName"]
                                    elif indexType == "NumberLiteral":
                                        value = obj["right"]["number"]
                                
                                elif type == "MemberAccess":
                                    parentMember = obj["right"]["expression"]["name"]
                                    childMember = obj["right"]["memberName"]

                                elif type == "Identifier":
                                    baseName = obj["right"]["name"]

                                elif type == "NumberLiteral":
                                    value = obj["right"]["number"]

                                elif type == "BooleanLiteral":
                                    value = obj["right"]["value"]

                                right = Operator(type,value,baseName,indexType,parentMember,childMember)
                            
                        else:
                            value = "False" if dataType == "bool" else "0"

                        allLocalVariable.append(LocalVariable(dataType,varName,storageLoc,value,intializeType,parentMember,childMember,baseName,indexType,operator,left,right))

            functionExpression[funcName] = allExpression
            functionLocalVariable[funcName] = allLocalVariable

    return allMethods,functionExpression,functionLocalVariable


    # for method in allMethods:
        # print(method.funcName)
        # if len(method.parameterList) != 0:
        #     for par in method.parameterList:
        #         print(par.type)
        #         print(par.dataType)
        #         print(par.varName)
        #         print(par.storageLocation)
        #         print(par.isStateVar)
        #         print()
        # if len(method.returnParameterList) != 0:
        #     par = method.returnParameterList[0]
        #     print(par.type)
        #     print(par.dataType)
        #     print(par.varName)
        #     print(par.storageLocation)
        #     print(par.isStateVar)
        #     print()
            
    # for key in functionExpression:
    #     print("Method Name : " + key)
    #     for exp in functionExpression[key]:
    #         print(exp.type)
    #         print(exp.operator)
    #         print(exp.left.type)
    #         print(exp.left.value)
    #         print(exp.left.baseName)#varName
    #         print(exp.left.indexType)
    #         print(exp.left.parentMember)
    #         print(exp.left.childMember)
    #         print()
        
    # for key in functionLocalVariable:
    #     print(key)
    #     for exp in functionLocalVariable[key]:
    #         print(exp.dataType)
    #         print(exp.varName)
    #         print(exp.storageLoc)
    #         print(exp.value)
    #         print(exp.intializeType)
    #         print(exp.parentMember)
    #         print(exp.childMember)
    #         print(exp.baseName)
    #         print(exp.indexType)
    #         print(exp.operator)
    #         if exp.left != "None":
    #             print(exp.left.type)
    #             print(exp.left.value)
    #             print(exp.left.baseName)#varName
    #             print(exp.left.indexType)
    #             print(exp.left.parentMember)
    #             print(exp.left.childMember)
    #         if exp.right != "None":
    #             print(exp.right.type)
    #             print(exp.right.value)
    #             print(exp.right.baseName)#varName
    #             print(exp.right.indexType)
    #             print(exp.right.parentMember)
    #             print(exp.right.childMember)
    #         print()

if __name__ == "__main__":
    method_Information()