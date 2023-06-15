import os
from langchain.document_loaders import TextLoader
os.environ['OPENAI_API_KEY']='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'
loader = TextLoader('./yt.txt')

from langchain.indexes import VectorstoreIndexCreator
index = VectorstoreIndexCreator().from_loaders([loader])

query = "What is the document about?"
print(index.query(query))

# from langchain.indexes import VectorstoreIndexCreator
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.docstore.document import Document

# text = """"""

# def cb(body):
#     text_splitter = CharacterTextSplitter()

#     texts = text_splitter.split_text(body)

#     docs = [Document(page_content=t) for t in texts[:3]]

#     index = VectorstoreIndexCreator().from_loaders([docs])

#     query = "What is the document about?"
#     print(index.query(query))

# cb(text)