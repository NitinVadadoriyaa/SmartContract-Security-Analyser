
def stateVariable():
    import env
    import build_json
    from enum import Enum

    fileName = env.fileName
    jsonFileName = fileName.rsplit('.',1)[0] + "_ast.json"
    jsonObject = build_json.build_json(jsonFileName)
    # print(jsonObject)

    methods = jsonObject["children"][1]["subNodes"]
    
    class Parameter:
        def __init__(self,type,dataType,varName,storageLocation,isStateVar):
            self.type = type
            self.dataType = dataType
            self.varName = varName
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

    mapping = {}


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
            if len(key["body"]["statements"]) != 0: #------All Expression of individual function------#
                statements = key["body"]["statements"]
                for obj in statements:
                    expType = "None"
                    expOperator = "None"
                    expLeft = "None"
                    expRight = "None"
                    
                    type = "None"
                    value = "None"
                    baseName = "None"
                    indexType = "None"
                    parentMember = "None"
                    childMember = "None"
                    #----- LEFT --------#
                    if obj["type"] == "ExpressionStatement":
                        obj = obj["expression"]
                        expType = obj["type"]
                        if expType == "BinaryOperation": #----Only binary operation----#

                            expOperator = obj["operator"]
                            
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
            mapping[funcName] = allExpression


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
            
    for key in mapping:
        for exp in mapping[key]:
            print(exp.type)
            print(exp.operator)
            print(exp.left.type)
            print(exp.left.value)
            print(exp.left.baseName)#varName
            print(exp.left.indexType)
            print(exp.left.parentMember)
            print(exp.left.childMember)
            print()

if __name__ == "__main__":
    stateVariable()