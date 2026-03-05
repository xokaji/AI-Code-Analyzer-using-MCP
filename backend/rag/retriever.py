def store_chunks(chunks):

    from backend.rag.embeddings import embed
    from backend.rag.vector_store import get_collection

    collection = get_collection()

    vectors = embed(chunks)

    for i, chunk in enumerate(chunks):

        collection.add(
            ids=[str(i)],
            embeddings=[vectors[i]],
            documents=[chunk]
        )

def retrieve(query):

    from backend.rag.embeddings import embed
    from backend.rag.vector_store import get_collection

    collection = get_collection()

    count = collection.count()
    if count == 0:
        return "(no indexed code available — upload or index a project first)"

    q = embed([query])[0]

    results = collection.query(
        query_embeddings=[q],
        n_results=min(5, count)
    )

    return results["documents"]