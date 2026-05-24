import json
from pathlib import Path
from langchain_core.documents import Document

_DEFAULT_CORPUS = Path(__file__).parent.parent / "data" / "corpus" / "sample_corpus.json"


def load_corpus(path: str | Path = _DEFAULT_CORPUS) -> list[Document]:
    """Load demographic JSON corpus into LangChain Documents."""
    with open(path) as f:
        entries = json.load(f)

    docs = []
    for entry in entries:
        page_content = f"{entry['title']}\n\n{entry['content']}"
        metadata = {
            "id": entry["id"],
            "title": entry["title"],
            "year": entry["year"],
            "country": entry.get("country", ""),
            "region": entry.get("region", ""),
            "source_org": entry.get("source_org", ""),
            "publication": entry.get("publication", ""),
            "topic": entry.get("topic", ""),
            "metric_years": entry.get("metric_years", []),
            "metric_values": entry.get("metric_values", []),
            "metric_label": entry.get("metric_label", ""),
        }
        docs.append(Document(page_content=page_content, metadata=metadata))

    return docs
