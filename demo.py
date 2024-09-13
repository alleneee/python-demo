from langchain.prompts import PromptTemplate

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import (
    AIMessage,  # 等价于OpenAI接口中的assistant role
    HumanMessage,  # 等价于OpenAI接口中的user role
    SystemMessage  # 等价于OpenAI接口中的system role
)

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

llm = ChatOpenAI(model="gpt-4o-mini",
                 openai_api_key="sk-d1SRuFYdIhUPQCKf4d2c1dCe9aC64aC3B1EaCa56Bb901e26",
                 openai_api_base="https://api.bianxie.ai/v1"
                 )
# response = llm.invoke("给我讲个动物的笑话")
# print(response.content)

messages = [
    SystemMessage(content="你是AGIClass的课程助理。"),
    HumanMessage(content="我是学员，我叫王卓然。"),
    AIMessage(content="欢迎！"),
    HumanMessage(content="我是谁")
]
# Prompt 模板封装
template  = PromptTemplate.from_template("给我讲个关于{subject}的笑话")
ret = llm.invoke(template.format(subject='鲨鱼'))

# ChatPromptTemplate 用模板表示的对话上下文
# template = ChatPromptTemplate.from_messages(
#     [
#         SystemMessagePromptTemplate.from_template(
#             "你是{product}的客服助手。你的名字叫{name}"),
#         HumanMessagePromptTemplate.from_template("{query}"),
#     ]
# )
# MessagesPlaceholder 把多轮对话变成模板
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
human_prompt = "Translate your answer to {language}."
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)

chat_prompt = ChatPromptTemplate.from_messages(
    # variable_name 是 message placeholder 在模板中的变量名
    # 用于在赋值时使用
    [MessagesPlaceholder("history"), human_message_template]
)

# ret = llm.invoke(messages)

print(ret.content)

if __name__ == '__main__':
    print()