import os
from pathlib import Path

from backend.config.settings import settings


_collection = None


def get_collection():

	global _collection

	if _collection is not None:
		return _collection

	try:
		import chromadb
	except ImportError as e:
		raise RuntimeError(
			"Missing optional dependency 'chromadb'. Install it with: pip install chromadb"
		) from e

	repo_root = Path(__file__).resolve().parents[2]
	persist_path = Path(settings.VECTOR_DB_PATH)
	if not persist_path.is_absolute():
		persist_path = repo_root / persist_path

	os.makedirs(persist_path, exist_ok=True)

	client = chromadb.PersistentClient(path=str(persist_path))
	_collection = client.get_or_create_collection("code")
	return _collection