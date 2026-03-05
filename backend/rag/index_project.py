from backend.rag.chunker import chunk_project
from backend.rag.retriever import store_chunks

def index_project(project_path):

    chunks = chunk_project(project_path)

    store_chunks(chunks)

    return len(chunks)