from unittest.mock import MagicMock
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_classic.retrievers.ensemble import EnsembleRetriever
from rag.retriever import build_retriever


class _FakeRetriever(BaseRetriever):
    k: int = 6

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list[Document]:
        return []


def _mock_chroma():
    chroma = MagicMock()
    chroma.as_retriever.return_value = _FakeRetriever()
    return chroma


def _mock_bm25():
    return _FakeRetriever(k=6)


def test_returns_ensemble():
    assert isinstance(build_retriever(_mock_chroma(), _mock_bm25()), EnsembleRetriever)


def test_two_retrievers():
    r = build_retriever(_mock_chroma(), _mock_bm25())
    assert len(r.retrievers) == 2


def test_weights_sum_to_one():
    r = build_retriever(_mock_chroma(), _mock_bm25())
    assert abs(sum(r.weights) - 1.0) < 1e-6


def test_custom_weights():
    r = build_retriever(_mock_chroma(), _mock_bm25(), bm25_weight=0.5, vector_weight=0.5)
    assert r.weights == [0.5, 0.5]


def test_k_set_on_bm25():
    bm25 = _mock_bm25()
    build_retriever(_mock_chroma(), bm25, k=4)
    assert bm25.k == 4
