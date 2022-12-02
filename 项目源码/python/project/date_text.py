import json
import os
def add_json():
    data={
        "host" : "127.0.0.1",
        "user" : "root",
        "password" : "123456",
        "db" : "test",
        "charset" : "utf8"
    }
    if not os.path.exists("auto.json"):
        json_str=json.dumps(data,indent=4)
        with open("auto.json" ,"w")as f:f.write(json_str)
add_json()