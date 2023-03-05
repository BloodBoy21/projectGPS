import ujson

with open("../env.json", "r") as f:
    json_data = f.read()
    data_dict = ujson.loads(json_data)
    print(data_dict)


def get_env(key):
    return data_dict[key]

def set_env(key, value):
    data_dict[key] = value
    with open("data.json", "w") as f:
        f.write(ujson.dumps(data_dict))