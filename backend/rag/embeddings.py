_model = None


def _get_model():

    global _model

    if _model is not None:
        return _model

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        raise RuntimeError(
            "Missing optional dependency 'sentence-transformers'. "
            "Install it with: pip install sentence-transformers"
        ) from e

    _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed(texts):

    model = _get_model()
    return model.encode(texts)