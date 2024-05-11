
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
        def __init__(self,type,dataType,varName,isParameter,storageLocation,isStateVar):
            self.type = type
            self.dataType = dataType
            self.varName = varName#variable name
            self.isParameter = True
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
        def __init__(self,dataType,isParameter,varName,storageLoc,value,intializeType,parentMember,childMember,baseName,indexType,operator,left,right):
            self.dataType = dataType
            self.isParameter = False
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

    class ConditionStatment:
        def __init__(self,type,operator,left,right):
            self.type = type
            self.operator = operator
            self.left = left
            self.right = right
    
    #----------{Index : Array Of All Present ConditionStatment-----------------#
    AllConditionStatment = []

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
                    parameterList.append(Parameter(obj["typeName"]["type"],obj["typeName"]["name"],obj["name"],False,obj["storageLocation"],obj["isStateVar"]))

            if len(key["returnParameters"]) != 0: #--- return parameters ---#
                obj = key["returnParameters"]["parameters"][0]
                returnParameterList.append(Parameter(obj["typeName"]["type"],obj["typeName"]["name"],obj["name"],False,obj["storageLocation"],obj["isStateVar"]))
            
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
                                if "name" in obj["left"]["base"]:
                                    baseName = obj["left"]["base"]["name"]
                                indexType = obj["left"]["index"]["type"]

                                if indexType == "MemberAccess":
                                    parentMember = obj["left"]["index"]["expression"]["name"]
                                    baseName = parentMember
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

                            elif type == "BinaryOperation": #-- a = a + b --#
                                obj = obj["right"]
                                if obj["operator"] == "+":
                                    expOperator = "+="
                                elif obj["operator"] == "-":
                                    expOperator = "-="
                                elif obj["operator"] == "*":
                                    expOperator = "*="
                                elif obj["operator"] == "/":
                                    expOperator = "/="

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
                        
                        elif expType == "FunctionCall": #writen only for send Token[DOS attack]
                            expOperator = "None"
                            tempDict = {
                            "isSender" : "None",
                            "isTransfer" : "None"
                            }
                            inDepthCall(obj,tempDict) #adding in LEFT-Operator
                            type = "None" # isTransfer
                            childMember = "None" # isSender
                            value = "None"
                            baseName = "None"
                            indexType = "None"
                            parentMember = "None"
                            
                            if tempDict["isTransfer"] != "None":
                                type = tempDict["isTransfer"]
                            if tempDict["isSender"] != "None": #TODO : data-dependency possible - caller address can be store in other name.
                                childMember = tempDict["isSender"]
                            
                            expLeft = Operator(type,value,baseName,indexType,parentMember,childMember)
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
                        if "name" in obj1["typeName"]:
                            dataType = obj1["typeName"]["name"]
                        else:
                            dataType = obj1["typeName"]["namePath"]

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
                                baseName = value

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
                                        print("left + member")
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

                        allLocalVariable.append(LocalVariable(dataType,False,varName,storageLoc,value,intializeType,parentMember,childMember,baseName,indexType,operator,left,right))

                    elif obj["type"] == "IfStatement":#--------Only Local Variable--------#
                        type = obj["condition"]["type"]
                        operator = obj["condition"]["operator"]
                        
                        #----- LEFT --------#
                        Lefttype = "None"
                        value = "None"
                        baseName = "None"
                        indexType = "None"
                        parentMember = "None"
                        childMember = "None"
                        
                        obj = obj["condition"]
                        Lefttype = obj["left"]["type"]
                        if Lefttype == "IndexAccess":
                            baseName = obj["left"]["base"]["name"]
                            indexType = obj["left"]["index"]["type"]

                            if indexType == "MemberAccess":
                                parentMember = obj["left"]["index"]["expression"]["name"]
                                childMember = obj["left"]["index"]["memberName"]
                            elif indexType == "NumberLiteral":
                                value = obj["left"]["number"]
                                
                        elif Lefttype == "MemberAccess":
                                parentMember = obj["left"]["expression"]["name"]
                                childMember = obj["left"]["memberName"]

                        elif Lefttype == "Identifier":
                                baseName = obj["left"]["name"]

                        elif Lefttype == "NumberLiteral":
                                value = obj["left"]["number"]

                        elif Lefttype == "BooleanLiteral":
                                value = obj["left"]["value"]

                        left = Operator(Lefttype,value,baseName,indexType,parentMember,childMember)


                        #----- RIGHT --------#
                        Righttype = "None"
                        value = "None"
                        baseName = "None"
                        indexType = "None"
                        parentMember = "None"
                        childMember = "None"
                        
                        Righttype = obj["right"]["type"]
                        if Righttype == "IndexAccess":
                            baseName = obj["right"]["base"]["name"]
                            indexType = obj["right"]["index"]["type"]

                            if indexType == "MemberAccess":
                                parentMember = obj["right"]["index"]["expression"]["name"]
                                childMember = obj["right"]["index"]["memberName"]
                            elif indexType == "NumberLiteral":
                                value = obj["right"]["number"]
                                
                        elif Righttype == "MemberAccess":
                                parentMember = obj["right"]["expression"]["name"]
                                childMember = obj["right"]["memberName"]

                        elif Righttype == "Identifier":
                                baseName = obj["right"]["name"]

                        elif Righttype == "NumberLiteral":
                                value = obj["right"]["number"]

                        elif Righttype == "BooleanLiteral":
                                value = obj["right"]["value"]

                        right = Operator(Righttype,value,baseName,indexType,parentMember,childMember)
                        cond = ConditionStatment(type,operator,left,right)
                        AllConditionStatment.append(cond) #condition statement

            functionExpression[funcName] = allExpression
            functionLocalVariable[funcName] = allLocalVariable

    return allMethods,functionExpression,functionLocalVariable,AllConditionStatment


    # for method in allMethods:
    #     print(method.funcName)
    #     print(method.visibility)
    #     print(method.stateMutability)
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
    #         print('---left---')
    #         print(exp.left.type)
    #         print(exp.left.value)
    #         print(exp.left.baseName)#varName
    #         print(exp.left.indexType)
    #         print(exp.left.parentMember)
    #         print(exp.left.childMember)
    #         print('---right---')
    #         print(exp.right.type)
    #         print(exp.right.value)
    #         print(exp.right.baseName)#varName
    #         print(exp.right.indexType)
    #         print(exp.right.parentMember)
    #         print(exp.right.childMember)
    #         print()
        
    for key in functionLocalVariable:
        print(key)
        print()
        # print(len(functionLocalVariable[key]))
        for exp in functionLocalVariable[key]:
            print(exp.dataType)
            print(exp.varName)
            print(exp.storageLoc)
            print(exp.value)
            print(exp.intializeType)
            print(exp.parentMember)
            print(exp.childMember)
            print(exp.baseName)
            print(exp.indexType)
            print(exp.operator)
            if exp.left != "None":
                print(exp.left.type)
                print(exp.left.value)
                print(exp.left.baseName)#varName
                print(exp.left.indexType)
                print(exp.left.parentMember)
                print(exp.left.childMember)
            if exp.right != "None":
                print(exp.right.type)
                print(exp.right.value)
                print(exp.right.baseName)#varName
                print(exp.right.indexType)
                print(exp.right.parentMember)
                print(exp.right.childMember)
            print()

    # for exp in AllConditionStatment:  
    #     print(exp.type)
    #     print(exp.operator)
    #     print(exp.left.type)
    #     print(exp.left.value)
    #     print(exp.left.baseName)#varName
    #     print(exp.left.indexType)
    #     print(exp.left.parentMember)
    #     print(exp.left.childMember)
    #     print("-----------------")
    #     print(exp.right.type)
    #     print(exp.right.value)
    #     print(exp.right.baseName)#varName
    #     print(exp.right.indexType)
    #     print(exp.right.parentMember)
    #     print(exp.right.childMember)

def inDepthCall(obj,tempDict):
    if "arguments" in obj:
        for tempObj in obj["arguments"]:
            if "memberName" in tempObj:
                if tempObj["memberName"] == "transfer":
                    tempDict["isTransfer"] = "transfer"

                elif tempObj["memberName"] == "sender":
                    tempDict["isSender"] = "sender"

            elif "name" in tempObj: #For Data-Dependency
                tempDict["isSender"] = tempObj["name"]

            if "expression" in tempObj:
                inDepthCall(tempObj["expression"],tempDict)
        #for-loop-end

    if "memberName" in obj:
        if obj["memberName"] == "transfer":
            tempDict["isTransfer"] = "transfer"
            
        elif obj["memberName"] == "sender":
            tempDict["isSender"] = "sender"
           
    if "expression" in obj:
        inDepthCall(obj["expression"],tempDict)

      
if __name__ == "__main__":
    method_Information()