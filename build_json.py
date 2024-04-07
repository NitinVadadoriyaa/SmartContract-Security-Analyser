def build_json(fileName):
    import json

    # print(fileName)
    with open(f"/home/nitin/Desktop/Tool/{fileName}",'r') as file:
        jsonData = file.read()
        jsonObject = json.loads(jsonData)
    
        return jsonObject

    # print(jsonObject)
    # print()
    # print(jsonObject['type']) #for key : value
    # print(jsonObject['children'][0]['type']) #for key : value, value can be array of object.
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 build_json.py <fileName>")
        sys.exit(1)

    fileName = sys.argv[1]
    jsonObject = build_json(fileName)
    print(jsonObject)
    