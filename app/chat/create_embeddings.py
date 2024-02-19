from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import sys
import io

def create_embeddings_for_pdf(pdf_id: str, pdf_path: str):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    loader = PyPDFLoader(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    docs = loader.load_and_split(text_splitter)

    print(docs)






    # embedding = OpenAIEmbeddings()
    pass
