import os
import sys
import json
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv,find_dotenv
# 新版本推荐写法（兼容0.1.0+）
from typing import List, Optional        # 类型注解
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


# 解决Windows编码问题
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

_ = load_dotenv(find_dotenv())
api_key = os.getenv("ZIJIE_API_KEY")
base_url = "https://ark.cn-beijing.volces.com/api/v3"

# 2. 初始化原生 OpenAI 客户端（备用）
client = OpenAI(api_key=api_key, base_url=base_url)

# 3. 关键修复：ChatOpenAI 必须配置字节方舟的 base_url 和 api_key
# （之前的 ChatOpenAI 用了默认配置，指向 OpenAI 官方，国内访问超时）
chat = ChatOpenAI(
    model="doubao-1-5-lite-32k-250115",
    temperature=0.3,
    api_key=api_key,          # 指定字节方舟的 API Key
    base_url=base_url,        # 指定字节方舟的接口地址
    request_timeout=5000        # 全局超时，避免无限等待
)

def get_completion(prompt, model="doubao-1-5-lite-32k-250115"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # 这里我们设置为0，表示完全确定的输出
    )
    return response.choices[0].message.content.strip()


# customer_email = """
# Arrr, I be fuming that me blender lid \
# flew off and splattered me kitchen walls \
# with smoothie! And to make matters worse,\
# the warranty don't cover the cost of \
# cleaning up me kitchen. I need yer help \
# right now, matey!
# """

# style = """Chinese \
# in a calm and respectful tone
# """

# prompt = f"""Translate the text \
# that is delimited by triple backticks 
# into a style that is {style}.
# text: ```{customer_email}```
# """

# template_string = """Translate the text use Chinese \
# that is delimited by triple backticks \
# into a style that is {style}. 
# text: ```{text}```
# """
# customer_style = """CHinese \
# in a calm and respectful tone
# """

# prompt_template = ChatPromptTemplate.from_template(template_string)

# customer_messages = prompt_template.format_messages(
#                     style=customer_style,
#                     text=customer_email)



# print("开始调用模型...", time.time())
# try:
#     customer_response = chat.invoke(
#         customer_messages,
#         request_timeout=20         # 或直接在 ChatOpenAI 初始化时加
#     )
#     print("调用成功！", time.time())
#     print(customer_response.content)
# except Exception as e:
#     print("调用失败：", str(e))

customer_email = """
Arrr, I be fuming that me blender lid flew off and splattered me kitchen walls with smoothie! And to make matters worse, the warranty don't cover the cost of cleaning up me kitchen. I need yer help right now, matey!
"""
style = "Chinese in a calm and respectful tone"  # 简化风格描述，避免换行符问题

# 6. 修复模板字符串（去掉 \ 转义，格式更清晰）
template_string = """Translate the text into Chinese in a {style} tone.
The text to translate is delimited by triple backticks:
```{text}```
"""

# 7. 构建提示词模板
prompt_template = ChatPromptTemplate.from_template(template_string)
customer_messages = prompt_template.format_messages(
    style=style,
    text=customer_email
)

simple_prompt = f"Translate the following text into calm and respectful Chinese: {customer_email}"
native_result = get_completion(simple_prompt)
customer_response = chat.invoke(customer_messages)

service_reply = """Hey there customer, 
the warranty does not cover 
cleaning expenses for your kitchen 
because it's your fault that 
you misused your blender 
by forgetting to put the lid on before 
starting the blender. 
Tough luck! See ya!
"""

service_style_pirate = """
 polite tone 
"""

service_message=prompt_template.format_messages(
    style=service_style_pirate,
    text=service_reply
)

# print(service_message[0].content)
service_response = chat.invoke(service_message)
# print(service_response.content)
{
  "gift": False,
  "delivery_days": 5,
  "price_value": "pretty affordable!"
}

customer_review = """
This leaf blower is pretty amazing.  It has four settings:
candle blower, gentle breeze, windy city, and tornado. 
It arrived in two days, just in time for my wife's 
anniversary present. 
I think my wife liked it so much she was speechless. 
So far I've been the only one using it, and I've been 
using it every other morning to clear the leaves on our lawn. 
It's slightly more expensive than the other leaf blowers 
out there, but I think it's worth it for the extra features.
"""

review_template = """
For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? 
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product 
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price in CHinese,
and output them as a comma separated Python list.

Format the output as JSON with the following keys:
gift
delivery_days
price_value

text: {text}
"""

# prompt_template = ChatPromptTemplate.from_template(review_template)
# review_message = prompt_template.format_messages(text=customer_review)
# review_response = chat.invoke(review_message)
# print(review_response.content)


# 2. 定义你的ReviewAnalysis数据模型（补充完整字段）
class ReviewAnalysis(BaseModel):
    gift: bool = Field(description="是否是礼物，True/False")
    delivery_days: int = Field(description="到货天数，整数")
    price_value: List[str] = Field(description="价格和价值相关的评价，列表形式")

# 3. 初始化LLM模型（关键：替换为你的API Key）
# 注意：需要先安装依赖 pip install langchain-openai openai
llm = ChatOpenAI(
    model="doubao-1-5-lite-32k-250115",
    temperature=0.3,
    api_key=api_key,          # 指定字节方舟的 API Key
    base_url=base_url, # 替换为自己的API Key
)

# 4. 绑定结构化输出并调用
prompt = """
请严格按照以下要求输出：
1. 仅返回JSON字符串，不要任何解释、说明、前缀或后缀文字；
2. JSON必须包含以下字段：
   - gift：布尔值（true/false），表示是否是礼物；
   - delivery_days：整数，表示到货天数；
   - price_value：字符串数组，表示价格和价值相关评价；
3. 严格遵循JSON格式，使用双引号，字段名和值格式正确。

示例输出：
{
  "gift": true,
  "delivery_days": 3,
  "price_value": ["有点贵但质量好"]
}

现在分析这条评论：买来送老婆的，三天到货，有点贵但质量好
"""

# 6. 调用模型并解析结果（替代with_structured_output）
response = llm.invoke(prompt)
response_text = response.content.strip()  # 提取模型返回的文本
# 7. 解析JSON并转换为结构化模型
try:
    # 解析JSON字符串为字典
    result_dict = json.loads(response_text)
    # 转换为ReviewAnalysis对象（自动验证字段类型）
    result = ReviewAnalysis(**result_dict)
    
    # 输出结果（和你的原代码输出逻辑一致）
    print(result.gift)          # 输出：True
    print(result.delivery_days) # 输出：3
    print(result.price_value)   # 输出：['有点贵但质量好']
except json.JSONDecodeError as e:
    # 调试用：JSON解析失败时打印原始返回内容
    print(f"JSON解析失败：{e}")
    print(f"模型返回的原始内容：{response_text}")
except Exception as e:
    # 其他错误（如字段类型不匹配）
    print(f"数据验证失败：{e}")



# # 8. 测试调用（先验证原生调用，再验证 LangChain 调用）
# print("=== 第一步：测试原生 OpenAI 客户端调用 ===")

# print("原生调用结果：", native_result)

# print("\n=== 第二步：测试 LangChain ChatOpenAI 调用 ===")
# print("开始调用模型...", time.ctime())
# try:

#     print("调用成功！", time.ctime())
#     print("最终翻译结果：\n", customer_response.content, "\n\n", customer_response.usage_metadata)
# except Exception as e:
#     print("调用失败：", str(e))