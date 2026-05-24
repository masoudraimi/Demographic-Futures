import json
from langchain_core.documents import Document
from rag.loader import load_corpus


def test_returns_list_of_documents(sample_docs):
    assert isinstance(sample_docs, list)
    assert all(isinstance(d, Document) for d in sample_docs)


def test_correct_count(sample_docs):
    assert len(sample_docs) == 3


def test_page_content_contains_title(sample_docs):
    assert "Australia: Total Fertility Rate" in sample_docs[0].page_content


def test_page_content_contains_content(sample_docs):
    assert "replacement threshold" in sample_docs[0].page_content


def test_title_and_content_separated_by_newlines(sample_docs):
    assert "\n\n" in sample_docs[0].page_content


def test_metadata_id(sample_docs):
    assert sample_docs[0].metadata["id"] == "fert_aus_001"


def test_metadata_country(sample_docs):
    assert sample_docs[0].metadata["country"] == "Australia"


def test_metadata_source_org(sample_docs):
    assert sample_docs[0].metadata["source_org"] == "ABS"


def test_metadata_topic(sample_docs):
    assert sample_docs[0].metadata["topic"] == "fertility"


def test_metadata_metric_years(sample_docs):
    assert sample_docs[0].metadata["metric_years"] == [2000, 2010, 2022]


def test_metadata_metric_values(sample_docs):
    assert sample_docs[0].metadata["metric_values"] == [1.75, 1.92, 1.58]


def test_metadata_metric_label(sample_docs):
    assert "Fertility" in sample_docs[0].metadata["metric_label"]


def test_empty_corpus_returns_empty_list(tmp_path):
    p = tmp_path / "empty.json"
    p.write_text("[]")
    assert load_corpus(p) == []


def test_missing_optional_fields(tmp_path):
    data = [{"id": "x", "title": "T", "content": "C", "year": 2020}]
    p = tmp_path / "minimal.json"
    p.write_text(json.dumps(data))
    docs = load_corpus(p)
    assert docs[0].metadata["country"] == ""
    assert docs[0].metadata["metric_years"] == []
    assert docs[0].metadata["metric_values"] == []
