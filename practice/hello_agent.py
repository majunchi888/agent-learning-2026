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

# 准备消息（用中文提问，模型支持多语言）
messages = [
    {
        "role": "user",
        "content": "你好，我是马马俊驰，请用中文自我介绍一下你的能力。"
    }
]

try:
    # 调用 Groq 的 chat completions 接口
    # 推荐模型：llama-3.1-70b-versatile（强大中文支持）或 llama-3.1-8b-instant（更快、更省额度）
    # 完整列表见：https://console.groq.com/docs/models （登录后查看最新）
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # 推荐这个：强大、支持长上下文、中文优秀
        # 备选模型："llama-3.1-8b-instant"（更快，适合测试）、"mixtral-8x7b-32768"、"gemma2-9b-it" 等
        messages=messages,
        temperature=0.7,                # 创造性，0.0-1.0
        max_tokens=500,
        stream=False                    # 非流式，一次性输出
    )

    # 打印完整响应
    print("Groq 回复：")
    print(response.choices[0].message.content.strip())
    print("\n使用 token：", response.usage.total_tokens if response.usage else "未知")

except Exception as e:
    print("调用失败：", str(e))