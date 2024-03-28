
def stateVariable():
    import env
    import build_json
    from enum import Enum

    fileName = env.fileName
    jsonFileName = fileName.rsplit('.',1)[0] + "_ast.json"
    jsonObject = build_json.build_json(jsonFileName)
    # print(jsonObject)

    stateVariable = jsonObject["children"][1]["subNodes"]

    #datatype --> value --- REMOVE IT ----
    class DataValue(Enum):
        bool = "value"
        uint8 = "number"
        uint16 = "number"
        uint32 = "number"
        uint64 = "number"
        uint128 = "number"
        uint256 = "number"
        address = "number"
        bytes1 = "number" #extend bytes1 -- bytes32
    
    #body for Integer-datatype
    class Integer:
        def __init__(self,dataType,varName,visibility,value = "0",operator = "None",left = "None",right = "None",funcName = "None"):
            self.dataType = dataType
            self.varName = varName
            self.visibility = visibility
            self.value = value
            self.operator = operator
            self.left = left
            self.right = right
            self.funcName = funcName

    stateVariables = []

    for key in stateVariable:
        if key["type"] == 'StateVariableDeclaration':
            # print(key["variables"]) #array
            mainObj = key["variables"][0]["typeName"]["type"]
            if mainObj == "ElementaryTypeName":
                dataType = key["variables"][0]["typeName"]["name"]
                if dataType == "string":
                    continue
                varName = key["variables"][0]["name"]
                visibility = "public" if key["variables"][0]["visibility"] == "default" else key["variables"][0]["visibility"]
                # visibility = key["variables"][0]["visibility"]
                if dataType == "bool":
                    value = "False"
                else:
                    value = "0"
                expression = key["variables"][0]["expression"]
                left = right = operator = funcName = "None"
                if expression is not None:
                    if expression["type"] == "BooleanLiteral":
                        value = expression["value"]
                    elif expression["type"] == "NumberLiteral":
                        value = expression["number"]
                    elif expression["type"] == "UnaryOperation":
                        if expression["operator"] == '-':
                            operator = "-"
                            value = expression["subExpression"]["number"]
                            right = expression["subExpression"]["number"]
                        elif expression["operator"] == '!':
                            operator = "!"
                            value = expression["subExpression"]["value"]
                            right = expression["subExpression"]["value"]
                    elif expression["type"] == "BinaryOperation":
                        operator = expression["operator"]
                        if expression["left"]["type"] == "NumberLiteral":
                            left = expression["left"]["number"]
                        elif expression["left"]["type"] == "FunctionCall":
                            left = "FunctionCall"
                            funcName = expression["left"]["expression"]["name"]
                        else:
                            left = expression["left"]["name"]
                        
                        if expression["right"]["type"] == "NumberLiteral":
                            right = expression["right"]["number"]
                        elif expression["right"]["type"] == "FunctionCall":
                            right = "FunctionCall"
                            funcName = expression["right"]["expression"]["name"]
                        else:
                            right = expression["right"]["name"]


                stateVariables.append(Integer(dataType,varName,visibility,value,operator,left,right,funcName))
    
    # for var in stateVariables:
    #     print("dataType : " + var.dataType)
    #     print("varName : " + var.varName)
    #     print("visibility : " + var.visibility)
    #     print( var.value)
    #     print("operator : " + var.operator)
    #     print("left : " + var.left)
    #     print("right : " + var.right)
    #     print("funcName : " + var.funcName)
    #     print()
    return stateVariables
            


if __name__ == "__main__":
    stateVariable()