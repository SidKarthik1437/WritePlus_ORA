from langchain.document_loaders import UnstructuredURLLoader
urls = [
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-8-2023",
    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-9-2023"
]

loader = UnstructuredURLLoader(urls=urls)