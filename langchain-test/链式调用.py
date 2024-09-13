from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List, Dict, Optional
from enum import Enum
import json



# 输出结构
class SortEnum(str, Enum):
    data = 'data'
    price = 'price'


class OrderingEnum(str, Enum):
    ascend = 'ascend'
    descend = 'descend'


class Semantics(BaseModel):
    name: Optional[str] = Field(description="流量包名称", default=None)
    price_lower: Optional[int] = Field(description="价格下限", default=None)
    price_upper: Optional[int] = Field(description="价格上限", default=None)
    data_lower: Optional[int] = Field(description="流量下限", default=None)
    data_upper: Optional[int] = Field(description="流量上限", default=None)
    sort_by: Optional[SortEnum] = Field(description="按价格或流量排序", default=None)
    ordering: Optional[OrderingEnum] = Field(description="升序或降序排列", default=None)


# Prompt 模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "将用户的输入解析成JSON表示。"),
        ("human", "{text}"),
    ]
)

# 模型
llm = ChatOpenAI(model="gpt-4o-mini",
                 openai_api_key="sk-d1SRuFYdIhUPQCKf4d2c1dCe9aC64aC3B1EaCa56Bb901e26",
                 openai_api_base="https://api.bianxie.ai/v1"
                 )

structured_llm = llm.with_structured_output(Semantics)

# LCEL 表达式
runnable = (
    {"text": RunnablePassthrough()} | prompt | structured_llm
)

# 直接运行
ret = runnable.invoke("不超过100元的流量大的套餐有哪些")
print(
    json.dumps(
        ret.dict(),
        indent = 4,
        ensure_ascii=False
    )
)

# 流式输出
# 在当前的文档中 LCEL 产生的对象，被叫做 runnable 或 chain，经常两种叫法混用。本质就是一个自定义调用流程
for s in runnable.stream("不超过100元的流量大的套餐有哪些"):
    print("流式输出:")
    print(s, end="", flush=True)

if __name__ == '__main__':
    print()