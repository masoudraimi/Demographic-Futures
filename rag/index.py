from __future__ import annotations

import pickle
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

_INDEX_DIR = Path(__file__).parent.parent / "data" / "indices"
_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def _get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=_EMBED_MODEL)


def build_indices(
    chunks: list[Document],
    index_dir: Path = _INDEX_DIR,
) -> tuple[Chroma, BM25Retriever]:
    chroma_dir = index_dir / "chroma"
    bm25_path = index_dir / "bm25.pkl"
    chroma_dir.mkdir(parents=True, exist_ok=True)

    embeddings = _get_embeddings()
    chroma = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(chroma_dir),
    )

    bm25 = BM25Retriever.from_documents(chunks)
    with open(bm25_path, "wb") as f:
        pickle.dump(bm25, f)

    return chroma, bm25


def load_indices(
    index_dir: Path = _INDEX_DIR,
) -> tuple[Chroma, BM25Retriever] | None:
    chroma_dir = index_dir / "chroma"
    bm25_path = index_dir / "bm25.pkl"

    if not chroma_dir.exists() or not bm25_path.exists():
        return None

    embeddings = _get_embeddings()
    chroma = Chroma(
        persist_directory=str(chroma_dir),
        embedding_function=embeddings,
    )
    with open(bm25_path, "rb") as f:
        bm25 = pickle.load(f)

    return chroma, bm25


def indices_exist(index_dir: Path = _INDEX_DIR) -> bool:
    return (index_dir / "chroma").exists() and (index_dir / "bm25.pkl").exists()
