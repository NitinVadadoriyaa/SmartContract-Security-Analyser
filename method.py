
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
            if len(key["parameters"]["parameters"]) != 0:
                for obj in key["parameters"]["parameters"]:
                    parameterList.append(Parameter(obj["typeName"]["type"],obj["typeName"]["name"],obj["name"],obj["storageLocation"],obj["isStateVar"]))

            if len(key["returnParameters"]) != 0:
                obj = key["returnParameters"]["parameters"][0]
                returnParameterList.append(Parameter(obj["typeName"]["type"],obj["typeName"]["name"],obj["name"],obj["storageLocation"],obj["isStateVar"]))

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