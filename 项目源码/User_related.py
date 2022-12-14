import json


def dict_to_json(dict_obj, name, Mycls=None):
    js_obj = json.dumps(dict_obj, cls=Mycls, indent=4)

    with open(name, 'w') as file_obj:
        file_obj.write(js_obj)

if __name__ == '__main__':
    content_list=(['Touch.mp3\n', '11.mp3\n', '22秒.mp3'])
    dict_obj = {'successed': True, 'List': content_list}
    dict_to_json(dict_obj, 'dict_to_json.json')