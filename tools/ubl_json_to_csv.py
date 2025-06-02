import json

# this script can be used to convert UBLs code list format .gc to a csv file
# first convert the .gc file to an json here: https://jsonformatter.org/xml-to-json
# convert it with this code here

with open('json.json') as f:
    d = json.load(f)
    c = d.get("CodeList")
    c = c.get("SimpleCodeList")
    c = c.get("Row")

    list = {}
    for value in c:
        v = value.get("Value")

        code = ""
        desc = ""
        name = ""

        for a in v:
            r = a["SimpleValue"]
            if a["_ColumnRef"] == "code":
               code = r
            elif a["_ColumnRef"] == "name":
               name = r
            elif a["_ColumnRef"] == "description":
               desc = r

        if list.get(code) == None:
            list[code] = "\"" + code + "\";\"" + name + "\";\"" + desc + "\""

    print("CODE;NAME;DESCRIPTION")
    for l in list:
        a = list[l]
        print(a)