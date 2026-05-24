from unittest.mock import MagicMock, patch
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda


def _docs():
    return [Document(
        page_content="Japan's 65+ share reached 29.1% in 2022.",
        metadata={"source_org": "OECD", "country": "Japan", "publication": "Society at a Glance 2023", "year": 2022},
    )]


def test_build_chain_returns_runnable():
    from rag.pipeline import build_chain
    r = MagicMock()
    with patch("rag.pipeline.get_llm", return_value=MagicMock()):
        assert build_chain(r) is not None


def test_build_chain_with_sources_returns_runnable():
    from rag.pipeline import build_chain_with_sources
    r = MagicMock()
    with patch("rag.pipeline.get_llm", return_value=MagicMock()):
        assert build_chain_with_sources(r) is not None


def test_chain_with_sources_has_answer_and_sources():
    from rag.pipeline import build_chain_with_sources
    r = MagicMock()
    with patch("rag.pipeline.get_llm", return_value=RunnableLambda(lambda x: "mocked")):
        chain = build_chain_with_sources(r)
    result = chain.invoke("How old is Japan?")
    assert "answer" in result
    assert "sources" in result


def test_format_docs_includes_org_country_year():
    from rag.pipeline import _format_docs
    out = _format_docs(_docs())
    assert "OECD" in out
    assert "Japan" in out
    assert "2022" in out


def test_format_docs_multiple_docs_separated():
    from rag.pipeline import _format_docs
    docs = [
        Document(page_content="A", metadata={"source_org": "ABS", "country": "Australia", "publication": "p1", "year": 2022}),
        Document(page_content="B", metadata={"source_org": "OECD", "country": "Japan", "publication": "p2", "year": 2023}),
    ]
    assert "---" in _format_docs(docs)


def test_format_docs_empty():
    from rag.pipeline import _format_docs
    assert _format_docs([]) == ""
