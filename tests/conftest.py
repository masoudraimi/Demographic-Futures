import json
import pytest
from pathlib import Path
from langchain_core.documents import Document


@pytest.fixture()
def sample_json(tmp_path) -> Path:
    data = [
        {
            "id": "fert_aus_001",
            "title": "Australia: Total Fertility Rate 2000-2022",
            "content": "Australia's TFR declined from 1.75 in 2000 to 1.58 in 2022, below the 2.1 replacement threshold.",
            "year": 2022,
            "country": "Australia",
            "region": "Oceania",
            "source_org": "ABS",
            "publication": "Births, Australia 2022",
            "topic": "fertility",
            "metric_years": [2000, 2010, 2022],
            "metric_values": [1.75, 1.92, 1.58],
            "metric_label": "Total Fertility Rate",
        },
        {
            "id": "aging_jpn_001",
            "title": "Japan: World's Most Aged Society 2000-2022",
            "content": "Japan's 65+ share reached 29.1% in 2022, the highest of any country globally.",
            "year": 2022,
            "country": "Japan",
            "region": "East Asia",
            "source_org": "OECD",
            "publication": "Society at a Glance 2023",
            "topic": "aging",
            "metric_years": [2000, 2010, 2022],
            "metric_values": [17.4, 23.0, 29.1],
            "metric_label": "Population aged 65+ (%)",
        },
        {
            "id": "migr_can_001",
            "title": "Canada: Record Immigration Targets 2000-2022",
            "content": "Canada admitted 431,645 permanent residents in 2022, a record high under multi-year immigration targets.",
            "year": 2022,
            "country": "Canada",
            "region": "North America",
            "source_org": "Statistics Canada",
            "publication": "Annual Report to Parliament 2022",
            "topic": "migration",
            "metric_years": [2000, 2010, 2022],
            "metric_values": [227, 281, 432],
            "metric_label": "Permanent Residents Admitted (thousands)",
        },
    ]
    p = tmp_path / "corpus.json"
    p.write_text(json.dumps(data))
    return p


@pytest.fixture()
def sample_docs(sample_json) -> list[Document]:
    from rag.loader import load_corpus
    return load_corpus(sample_json)


@pytest.fixture()
def sample_chunks(sample_docs) -> list[Document]:
    from rag.chunker import chunk_documents
    return chunk_documents(sample_docs)
