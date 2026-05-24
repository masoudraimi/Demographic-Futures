"""RAGAS evaluation runner.

Run with:
    uv run python -m eval.runner
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

from eval.dataset import EVAL_QUESTIONS
from rag import (
    build_chain_with_sources,
    build_indices,
    build_retriever,
    chunk_documents,
    load_corpus,
    load_indices,
)
from rag.index import indices_exist

_RESULTS_DIR = Path(__file__).parent / "results"


def _get_or_build_retriever():
    docs = load_corpus()
    chunks = chunk_documents(docs)
    if indices_exist():
        chroma, bm25 = load_indices()
    else:
        chroma, bm25 = build_indices(chunks)
    return build_retriever(chroma, bm25)


def run_evaluation(output_path: Path | None = None) -> dict:
    retriever = _get_or_build_retriever()
    chain = build_chain_with_sources(retriever)

    questions, answers, contexts, ground_truths = [], [], [], []

    for item in EVAL_QUESTIONS:
        result = chain.invoke(item["question"])
        questions.append(item["question"])
        answers.append(result["answer"])
        contexts.append([doc.page_content for doc in result["sources"]])
        ground_truths.append(item["ground_truth"])

    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })

    scores = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    )

    result_df = scores.to_pandas()
    result_df["question"] = questions
    result_df["ground_truth"] = ground_truths

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = output_path or _RESULTS_DIR / f"eval_{timestamp}.json"
    result_df.to_json(save_path, orient="records", indent=2)
    result_df.to_json(_RESULTS_DIR / "latest.json", orient="records", indent=2)

    return {
        "faithfulness": float(result_df["faithfulness"].mean()),
        "answer_relevancy": float(result_df["answer_relevancy"].mean()),
        "context_precision": float(result_df["context_precision"].mean()),
        "context_recall": float(result_df["context_recall"].mean()),
        "n_questions": len(questions),
    }


if __name__ == "__main__":
    print(json.dumps(run_evaluation(), indent=2))
