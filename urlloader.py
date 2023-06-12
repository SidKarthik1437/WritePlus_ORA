from langchain.document_loaders import UnstructuredURLLoader,SeleniumURLLoader
from langchain.text_splitter import CharacterTextSplitter
urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://goo.gl/maps/NDSHwePEyaHMFGwh8"
]

loader = SeleniumURLLoader(urls=urls)
data = loader.load()

# ts = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)

# docs = ts.split_documents(data)

print(data)