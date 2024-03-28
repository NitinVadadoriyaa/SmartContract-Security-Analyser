
def stateVariable():
    import env
    import build_json
    from enum import Enum

    fileName = env.fileName
    jsonFileName = fileName.rsplit('.',1)[0] + "_ast.json"
    jsonObject = build_json.build_json(jsonFileName)
    # print(jsonObject)

    methods = jsonObject["children"][1]["subNodes"]
    
    class Method:
        def __init__(self,funcName,visibility,isConstructor,isFallback,isReceive,stateMutability = "None"):
            self.funcName = funcName
            self.visibility = visibility
            self.isConstructor = isConstructor
            self.isFallback = isFallback
            self.isReceive = isReceive
            self.stateMutability = stateMutability

    allMethods = []

    for key in methods:
        if key["type"] == "FunctionDefinition":
            funcName = key["name"]
            visibility = key["visibility"]
            isConstructor = key["isConstructor"]
            isFallback = key["isFallback"]
            isReceive = key["isReceive"]
            if  key["stateMutability"] != "null":
                stateMutability = key["stateMutability"]

            allMethods.append(Method(funcName,visibility,isConstructor,isFallback,isReceive,stateMutability))

    for method in allMethods:
        print(method.stateMutability)


    
            


if __name__ == "__main__":
    stateVariable()