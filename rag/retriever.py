from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers.ensemble import EnsembleRetriever

_DEFAULT_K = 6
_BM25_WEIGHT = 0.3
_VECTOR_WEIGHT = 0.7


def build_retriever(
    chroma: Chroma,
    bm25: BM25Retriever,
    k: int = _DEFAULT_K,
    bm25_weight: float = _BM25_WEIGHT,
    vector_weight: float = _VECTOR_WEIGHT,
) -> EnsembleRetriever:
    bm25.k = k
    chroma_retriever = chroma.as_retriever(search_kwargs={"k": k})
    return EnsembleRetriever(
        retrievers=[bm25, chroma_retriever],
        weights=[bm25_weight, vector_weight],
    )
