import json
from pathlib import Path
from langchain_core.documents import Document

_DEFAULT_CORPUS = Path(__file__).parent.parent / "data" / "corpus" / "sample_corpus.json"


def load_corpus(path: str | Path = _DEFAULT_CORPUS) -> list[Document]:
    """Load demographic JSON corpus into LangChain Documents."""
    with open(path, encoding="utf-8") as f:
        entries = json.load(f)

    docs = []
    for entry in entries:
        page_content = f"{entry['title']}\n\n{entry['content']}"
        metric_years = entry.get("metric_years") or None
        metric_values = entry.get("metric_values") or None
        metadata = {
            "id": entry["id"],
            "title": entry["title"],
            "year": entry["year"],
            "country": entry.get("country", ""),
            "region": entry.get("region", ""),
            "source_org": entry.get("source_org", ""),
            "publication": entry.get("publication", ""),
            "topic": entry.get("topic", ""),
            "metric_label": entry.get("metric_label", ""),
        }
        if metric_years is not None:
            metadata["metric_years"] = metric_years
        if metric_values is not None:
            metadata["metric_values"] = metric_values
        docs.append(Document(page_content=page_content, metadata=metadata))

    return docs
