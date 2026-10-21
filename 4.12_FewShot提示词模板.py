# 0. 导包
from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

# 1. 准备提示词数据
# 1.1 准备示例模板
example_template = PromptTemplate.from_template("单词：{word}, 反义词：{antonym}")

# 1.2 准备示例的数据（用来注入示例的提示词模板），格式：数组里套字典
examples_data = [
    {"word": "大", "antonym": "小"},
    {"word": "上", "antonym": "下"},
]

# 2. 创建few_shot提示词模板对象
few_shot_template = FewShotPromptTemplate(
    prefix="告知我单词的反义词，我提供如下的示例：",               # 示例之前的提示词，传入字符串
    example_prompt=example_template,                        # 示例的提示词模板，传入prompt类，结合通用提示词模板
    examples=examples_data,                                 # 示例的数据（用来注入示例的提示词模板），传入数组里套字典
    suffix="基于前面的示例告知我，{input_word}的反义词是？",      # 示例之后的提示词，传入字符串
    input_variables=['input_word']                          # 声明在prefix与suffix中所需要注入的变量名，传入列表
)

# 3. 使用invoke方法注入信息
prompt_text = few_shot_template.invoke(input={"input_word": "左"}).to_string()       # 由于我们想看提示词是什么，但是它返回的是prompt对象，所以需要使用to_string()转为字符串类型
print(prompt_text)

# 4. 创建模型对象
model = Tongyi(model="qwen-max")

# 5. 使用invoke方法调用模型，并输出模型返回结果
print(model.invoke(input=prompt_text))