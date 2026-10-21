# 0. 导包
import json

# 1. 字典 转 json
d = {
    "name": "周杰轮",
    "age": 11,
    "gender": "男"
}

# print(str(d))       # 单引号
s = json.dumps(d, ensure_ascii=False)
print(s, type(s))            # 双引号

# 2. 列表套字典 转 json
l = [
    {
        "name": "周杰轮",
        "age": 11,
        "gender": "男"
    },
    {
        "name": "蔡依临",
        "age": 12,
        "gender": "女"
    },
    {
        "name": "小明",
        "age": 16,
        "gender": "男"
    }
]

print(json.dumps(l, ensure_ascii=False))

# 3. json 转 字典、列表套字典
json_str = '{"name": "周杰轮", "age": 11, "gender": "男"}'
json_array_str = '[{"name": "周杰轮", "age": 11, "gender": "男"}, {"name": "蔡依临", "age": 12, "gender": "女"}, {"name": "小明", "age": 16, "gender": "男"}]'

res_dict = json.loads(json_str)
print(res_dict, type(res_dict))

res_list = json.loads(json_array_str)
print(res_list, type(res_list))