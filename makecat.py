import json
import os

data = {
    "paste": [

    ]
}

print("""
Choose a proper shell command: 

powershell: Get-ChildItem "data\cp*.json" | ForEach-Object -Process {echo $_.name} > files.txt
cmd: dir /b data\cp*.json > files.txt
bash: ls data/ > files.txt
----------------------------------------------------------------
**Don't forget to del the files(use delcat.py is ok)**
"""
)

f = open("files.txt", "r")
lines = f.readlines()
f.close()
count = 0
for line in lines:
    count += 1
    ff = open(("data/" + line).strip(), "r", encoding="utf-8")
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
print("Total: %d" % (count))
f = open("data.json", "w", encoding="utf-8")
json.dump(data, f, ensure_ascii=False, indent=4)