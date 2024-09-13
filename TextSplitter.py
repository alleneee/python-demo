from langchain_text_splitters import RecursiveCharacterTextSplitter

from DocumentLoaders import pages

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=100,
    length_function=len,
    add_start_index=True,
)

paragraphs = text_splitter.create_documents([pages[0].page_content])
for para in paragraphs:
    print(para.page_content)
    print('-------')

if __name__ == '__main__':
    print()