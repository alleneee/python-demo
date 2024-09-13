from pydantic import BaseModel, Field

# 定义你的输出对象
class Date(BaseModel):
    year: int = Field(description="Year")
    month: int = Field(description="Month")
    day: int = Field(description="Day")
    era: str = Field(description="BC or AD")

from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import PydanticOutputParser


model_name = 'gpt-4o-mini'
temperature = 0
llm = ChatOpenAI(model="gpt-4o-mini",
                 openai_api_key="sk-d1SRuFYdIhUPQCKf4d2c1dCe9aC64aC3B1EaCa56Bb901e26",
                 openai_api_base="https://api.bianxie.ai/v1"
                 )
# 定义结构化输出的模型
structured_llm = llm.with_structured_output(Date)

template = """提取用户输入中的日期。
用户输入:
{query}"""

prompt = PromptTemplate(
    template=template,
)

query = "2023年四月6日天气晴..."
input_prompt = prompt.format_prompt(query=query)

# print(structured_llm.invoke(input_prompt))


json_schema = {
    "title": "Date",
    "description": "Formated date expression",
    "type": "object",
    "properties": {
        "year": {
            "type": "integer",
            "description": "year, YYYY",
        },
        "month": {
            "type": "integer",
            "description": "month, MM",
        },
        "day": {
            "type": "integer",
            "description": "day, DD",
        },
        "era": {
            "type": "string",
            "description": "BC or AD",
        },
    },
}
structured_llm = llm.with_structured_output(json_schema)

#  输出指定格式的json
print(structured_llm.invoke(input_prompt))


# 使用 OutputParser 可以按指定格式解析模型的输出

from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser(pydantic_object=Date)

prompt = PromptTemplate(
    template="提取用户输入中的日期。\n用户输入:{query}\n{format_instructions}",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

input_prompt = prompt.format_prompt(query=query)
output = llm.invoke(input_prompt)
print("原始输出:\n"+output.content)

print("\n解析后:")
print(parser.invoke(output))

# `OutputFixingParser` 利用大模型做格式自动纠错

from langchain.output_parsers import OutputFixingParser

new_parser = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())

bad_output = output.content.replace("4","四")
print("PydanticOutputParser:")

try:
    parser.invoke(bad_output)
except Exception as e:
    print(e)

print("OutputFixingParser:")
print(new_parser.invoke(bad_output))


if __name__ == '__main__':
    print()