# groq_hello.py (或继续用 deepseek_hello.py，但建议改名避免混淆)
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取 API Key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("错误：未找到 GROQ_API_KEY，请检查 .env 文件")
    exit(1)

# 初始化 Groq 客户端（OpenAI 兼容接口）
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


raw_text = "今天是2026年3月5日，我们开会讨论了毕业论文进度。\
          小明负责文献综述部分，他说下周能完成初稿。\
          马俊驰你负责实验数据收集，记得在3月15日前把数据整理好发给导师。\
          李老师说论文结构要调整，摘要和结论要加强。\
          会议结束时间是下午4点，大家辛苦了。"

prompt = f"""
你是一个专业的会议记录整理助手。
请从以下会议文本中提取关键信息，并严格按照以下 JSON 格式输出，不要输出任何多余文字、解释或 Markdown：

{{
  "summary": "会议总结（一句话概括会议主要内容）",
  "action_items": ["任务描述 - 负责人", "任务描述 - 负责人", ...],
  "date": "YYYY-MM-DD"
}}

要求：
- summary：用一句话总结会议核心内容
- action_items：列出所有待办事项，格式严格为 "任务 - 负责人"，如果没有负责人就写 "未知" 或 "全体"
- date：提取会议日期，如果没有明确日期就写 "未知"
- 输出必须是纯 JSON，不能有 ```json 或其他包裹,你必须严格只输出以下 JSON 结构，不允许有任何前导/尾随换行、空格、```json 标记、解释文字或其他任何内容。
输出必须从第一个开始，到最后一个  结束，中间可以有缩进，但前后绝对不能有空行。


会议文本：
{raw_text}
"""


# 准备消息（用中文提问，模型支持多语言）
# messages = [
#     {
#         "role": "user",
#         "content": prompt
#     }
# ]




# try:
#     # 调用 Groq 的 chat completions 接口
#     # 推荐模型：llama-3.1-70b-versatile（强大中文支持）或 llama-3.1-8b-instant（更快、更省额度）
#     # 完整列表见：https://console.groq.com/docs/models （登录后查看最新）
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",  # 推荐这个：强大、支持长上下文、中文优秀
#         # 备选模型："llama-3.1-8b-instant"（更快，适合测试）、"mixtral-8x7b-32768"、"gemma2-9b-it" 等
#         messages=messages,
#         temperature=0.7,                # 创造性，0.0-1.0
#         max_tokens=500,
#         stream=False                    # 非流式，一次性输出

#     )

def get_completion(prompt):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
        max_tokens=500,
        stream=False
    )

    return response.choices[0].message.content.strip(), response.usage.total_tokens if response.usage else "未知"
   
def get_copletion_from_messages(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
        max_tokens=500,
        stream=False
    )

    return response.choices[0].message.content.strip(), response.usage.total_tokens if response.usage else "未知"

messages =  [  
{'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},    
{'role':'user', 'content':'tell me a joke'},   
{'role':'assistant', 'content':'Why did the chicken cross the road'},   
{'role':'user', 'content':'I don\'t know'}  ]

response=get_copletion_from_messages(messages)


try:

    # 打印完整响应
    print("Groq 回复：")
    # print(get_completion(prompt))
    print(response)


except Exception as e:
    print("调用失败：", str(e))