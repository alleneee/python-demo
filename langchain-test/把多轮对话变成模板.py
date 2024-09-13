from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

llm = ChatOpenAI(model="gpt-4o-mini",
                 openai_api_key="sk-d1SRuFYdIhUPQCKf4d2c1dCe9aC64aC3B1EaCa56Bb901e26",
                 openai_api_base="https://api.bianxie.ai"
                 )


# 把Prompt模板看作带有参数的函数
human_prompt = "Translate your answer to {language}."
human_message_template = HumanMessagePromptTemplate.from_template(human_prompt)

chat_prompt = ChatPromptTemplate.from_messages(
    # variable_name 是 message placeholder 在模板中的变量名
    # 用于在赋值时使用
    [MessagesPlaceholder("history"), human_message_template]
)


human_message = HumanMessage(content="Who is Elon Musk?")
ai_message = AIMessage(
    content="Elon Musk is a billionaire entrepreneur, inventor, and industrial designer"
)

messages = chat_prompt.format_prompt(
    # 对 "history" 和 "language" 赋值
    history=[human_message, ai_message], language="中文"
)

print(messages.to_messages())

result = llm.invoke(messages)
print(result.content)

if __name__ == '__main__':
    print()
