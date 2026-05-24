from langchain_core.documents import Document
from rag.chunker import chunk_documents


def test_returns_documents(sample_chunks):
    assert all(isinstance(c, Document) for c in sample_chunks)


def test_chunk_count_gte_doc_count(sample_docs, sample_chunks):
    assert len(sample_chunks) >= len(sample_docs)


def test_metadata_preserved(sample_chunks):
    ids = {c.metadata.get("id") for c in sample_chunks}
    assert "fert_aus_001" in ids


def test_metric_years_preserved_in_chunks(sample_chunks):
    aus = next(c for c in sample_chunks if c.metadata.get("id") == "fert_aus_001")
    assert aus.metadata["metric_years"] == [2000, 2010, 2022]


def test_chunk_size_respected(sample_docs):
    chunks = chunk_documents(sample_docs, chunk_size=100, chunk_overlap=10)
    assert all(len(c.page_content) <= 120 for c in chunks)


def test_empty_input():
    assert chunk_documents([]) == []


def test_single_short_doc_not_split():
    doc = Document(page_content="Short text.", metadata={"id": "x"})
    assert len(chunk_documents([doc], chunk_size=512, chunk_overlap=64)) == 1
