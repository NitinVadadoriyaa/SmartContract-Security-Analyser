
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
        def __init__(self,type,baseType,baseName,indexType,parentMember,childMember):
            self.type = type
            self.baseType = baseType
            self.baseName = baseName
            self.indexType = indexType
            self.parentMember = parentMember
            self.childMember = childMember
            
    class Expression:
        def __init__(self,type,operator,left,right):
            self.type = type
            self.operator = operator
            self.left = left
            self.right = right

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
            
            if len(key["body"]["statements"]) != 0:
                statements = key["body"]["statements"]
                for obj in statements:
                    expType = "None"
                    expOperator = "None"
                    expLeft = "None"
                    expRight = "None"
                    
                    type = "None"
                    baseType = "None"
                    baseName = "None"
                    indexType = "None"
                    parentMember = "None"
                    childMember = "None"
                    
                    if obj["type"] == "ExpressionStatement":
                        obj = obj["expression"]
                        expType = obj["type"]
                        expOperator = obj["operator"]
                        type = obj["left"]["type"]
                        
                        turn = "base"
                        if type == "IndexAccess":
                            turn = "base"
                        elif type == "MemberAccess":
                            turn = "expression"

                        baseType = "None" if turn in obj["left"] else obj["left"][turn]["type"]
                        baseName = "None" if turn in obj["left"] else obj["left"][turn]["name"]
                        indexType = "None" if "index" in obj["left"] else obj["left"]["index"]["type"]
                        if "index" in obj["left"]:
                            if "expression" in obj["left"]["index"]:
                                parentMember = obj["left"]["index"]["expression"]["name"]
                            childMember = obj["left"]["index"]["memberName"]
                        expLeft = Parameter(type,baseType,baseName,indexType,parentMember,childMember)

                        type = "None"
                        baseType = "None"
                        baseName = "None"
                        indexType = "None"
                        parentMember = "None"
                        childMember = "None"

                        type = obj["right"]["type"]
                        turn = "base"
                        if type == "IndexAccess":
                            turn = "base"
                        elif type == "MemberAccess":
                            turn = "expression"

                        baseType = "None" if turn in obj["right"] else obj["right"][turn]["type"]
                        baseName = "None" if turn in obj["right"] else obj["right"][turn]["name"]
                        indexType = "None" if "index" in obj["right"] else obj["right"]["index"]["type"]
                        if "index" in obj["right"]:
                            if "expression" in obj["right"]["index"]:
                                parentMember = obj["right"]["index"]["expression"]["name"]
                            childMember = obj["right"]["index"]["memberName"]
                        expLeft = Parameter(type,baseType,baseName,indexType,parentMember,childMember)


            allMethods.append(Method(funcName,visibility,isConstructor,isFallback,isReceive,stateMutability,parameterList,returnParameterList))

    for method in allMethods:
        print(method.funcName)
        if len(method.parameterList) != 0:
            for par in method.parameterList:
                print(par.type)
                print(par.dataType)
                print(par.varName)
                print(par.storageLocation)
                print(par.isStateVar)
                print()
        if len(method.returnParameterList) != 0:
            par = method.returnParameterList[0]
            print(par.type)
            print(par.dataType)
            print(par.varName)
            print(par.storageLocation)
            print(par.isStateVar)
            print()


    
            


if __name__ == "__main__":
    stateVariable()