from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import json

# 配置 OpenAI 的聊天模型
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key="your_openai_api_key",
    openai_api_base="https://api.bianxie.ai"
)

# 定义工具函数
@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

# 绑定工具到聊天模型
llm_with_tools = llm.bind_tools([add, multiply])

def main():
    query = "3的4倍是多少?"
    messages = [HumanMessage(content=query)]

    try:
        # 调用 OpenAI API
        output = llm_with_tools.invoke(messages)

        # 如果 output 是字符串类型，输出提示
        if isinstance(output, str):
            print("Output is a string:", output)
        elif hasattr(output, 'tool_calls'):
            print(json.dumps(output.tool_calls, indent=4))
        else:
            print("Output is not in the expected format:", output)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
