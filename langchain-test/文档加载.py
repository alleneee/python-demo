from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import ChatOpenAI

loader = PyMuPDFLoader("llama2.pdf")
pages = loader.load_and_split()

print(pages[0].page_content)



if __name__ == '__main__':
    print()