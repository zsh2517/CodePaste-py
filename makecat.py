import json

data = {
    "paste": [

    ]
}

f = open("files.txt", "r")
lines = f.readlines()
f.close()
for line in lines:
    ff = open(("data\\" + line).strip(), "r", encoding="utf-8")
    jsondata = json.load(ff)
    data["paste"].insert(0, {
        "pasteid": line.strip().split(".")[0],
        "length": len(jsondata["code"]), 
        "desc": "" if jsondata["desc"] == "No Description" else jsondata["desc"],
        "bgn": int(jsondata["bgn"]),
        "exp": -1 if jsondata["exp"] == "0" else jsondata["exp"],
        "user": "" if jsondata["user"] == "annoymous" else jsondata["user"],
        "lang": jsondata["lang"],
        "fname": "" if jsondata["fname"] == "code_file" else jsondata["fname"],
        "pwd": False if jsondata["pwd"] == "" else True 
    })

f = open("data.json", "w", encoding="utf-8")
json.dump(data, f, ensure_ascii=False, indent=4)