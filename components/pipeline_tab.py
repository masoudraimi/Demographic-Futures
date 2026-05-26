"""Pipeline tab, live RAG architecture visualiser.

Shows: architecture diagram, live retrieval trace, Pydantic schema,
and corpus stats. No LLM calls required for the trace.
"""

from __future__ import annotations

import json

import streamlit as st
from langchain_core.documents import Document

from palette import BG_CODE, GOLD, GREEN, ORANGE, TEXT_DIM, TEXT_HEADING, TEXT_MUTED, TEXT_SUBTLE


# ---------------------------------------------------------------------------
# Architecture diagram (Graphviz DOT)
# ---------------------------------------------------------------------------

_DOT = f"""
digraph rag {{
    rankdir=LR;
    bgcolor="transparent";
    node [fontname="sans-serif" fontsize=11 style="filled" fillcolor="#1a1a2e"
          fontcolor="{TEXT_HEADING}" color="{GOLD}" penwidth=1.5];
    edge [color="{GOLD}88" fontcolor="{TEXT_SUBTLE}" fontsize=10 fontname="sans-serif"];

    corpus  [label="JSON Corpus\\n(100 entries)"];
    loader  [label="Loader\\nLangChain Documents"];
    chunker [label="Chunker\\nRecursiveChar\\n512 chars / 64 overlap"];
    chroma  [label="ChromaDB\\n(persistent)\\nall-MiniLM-L6-v2" fillcolor="#0d2137"];
    bm25    [label="BM25Retriever\\n(keyword)" fillcolor="#1a2a1a"];
    ensemble[label="EnsembleRetriever\\nBM25 ×0.3  +  Vector ×0.7\\nk = 6" fillcolor="#1a1a3e"
             color="{ORANGE}" penwidth=2];
    prompt  [label="ChatPromptTemplate\\n(system + question)"];
    lcel    [label="LCEL Chain\\nRunnableParallel"];
    llm     [label="LLM Gateway\\nOpenRouter\\nGemini Flash 1.5" fillcolor="#2a1a1a"];
    pydantic[label="DemographicAnswer\\n(Pydantic v2)" color="{GREEN}" penwidth=2];
    out     [label="Structured Output\\nanswer · statistics\\nconfidence · data_gap"
             fillcolor="#0d2a0d" color="{GREEN}"];

    corpus  -> loader  -> chunker;
    chunker -> chroma;
    chunker -> bm25;
    chroma  -> ensemble;
    bm25    -> ensemble;
    ensemble -> lcel;
    ensemble -> prompt;
    prompt  -> lcel;
    lcel    -> llm;
    llm     -> pydantic -> out;
}}
"""


# ---------------------------------------------------------------------------
# Pydantic schema
# ---------------------------------------------------------------------------

_SCHEMA = {
    "class": "DemographicAnswer",
    "module": "rag.pipeline",
    "fields": {
        "answer": {"type": "str", "description": "Grounded narrative answer citing source org + year"},
        "key_statistics": {"type": "list[str]", "description": "Verbatim quantitative claims, e.g. 'TFR: 1.42 (ABS, 2022)'"},
        "countries_mentioned": {"type": "list[str]", "description": "ISO-3 country codes referenced in the answer"},
        "confidence": {"type": "Literal['high','medium','low']", "description": "high = context directly answers; medium = partial; low = mostly inferred"},
        "data_gap": {"type": "bool", "description": "True if context lacks sufficient data to fully answer the question"},
    },
    "source_file": "rag/pipeline.py",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _metric_card(label: str, value: str, sub: str = "") -> str:
    return f"""<div class="glass-card" style="text-align:center;padding:14px;">
        <div style="font-size:0.72rem;color:{TEXT_MUTED};text-transform:uppercase;letter-spacing:.06em;">{label}</div>
        <div style="font-size:1.8rem;font-weight:700;color:{GOLD};margin:4px 0;">{value}</div>
        <div style="font-size:0.75rem;color:{TEXT_DIM};">{sub}</div>
    </div>"""


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render_pipeline_tab(retriever, docs: list[Document], chunks: list[Document]) -> None:
    st.header("RAG Pipeline Architecture")
    st.caption(
        "A published hybrid retrieval system combining BM25 (keyword) and ChromaDB (dense vector) "
        "with structured Pydantic output. Everything here is live, the retrieval trace below "
        "invokes the actual EnsembleRetriever."
    )

    # ---- Corpus stats ------------------------------------------------------
    st.markdown("### Corpus overview")
    topics = sorted({d.metadata.get("topic", "") for d in docs if d.metadata.get("topic")})
    countries = sorted({d.metadata.get("country", "") for d in docs if d.metadata.get("country")})
    years = [d.metadata.get("year") for d in docs if d.metadata.get("year")]
    year_range = f"{min(years)}–{max(years)}" if years else "—"

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(_metric_card("Data entries", str(len(docs)), "JSON documents"), unsafe_allow_html=True)
    c2.markdown(_metric_card("Chunks indexed", str(len(chunks)), "512 chars / 64 overlap"), unsafe_allow_html=True)
    c3.markdown(_metric_card("Countries", str(len(countries)), "19 OECD peers"), unsafe_allow_html=True)
    c4.markdown(_metric_card("Year range", year_range, f"{len(topics)} topics"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Architecture diagram ----------------------------------------------
    st.markdown("### Pipeline architecture")
    st.graphviz_chart(_DOT, use_container_width=True)

    st.divider()

    # ---- Live retrieval trace ----------------------------------------------
    st.markdown("### Live retrieval trace")
    st.caption(
        "Type any question to invoke the EnsembleRetriever and inspect what the pipeline "
        "actually retrieves, before the LLM sees it."
    )

    query = st.text_input(
        "Query",
        placeholder="e.g. What is Australia's fertility rate?",
        key="pipeline_query",
    )

    if query:
        with st.spinner("Retrieving…"):
            try:
                retrieved = retriever.invoke(query)
            except Exception as e:
                st.error(f"Retrieval error: {e}")
                retrieved = []

        if not retrieved:
            st.warning("No documents retrieved.")
        else:
            st.success(f"Retrieved **{len(retrieved)}** documents (k=6, BM25 ×0.3 + Vector ×0.7)")
            for i, doc in enumerate(retrieved, 1):
                meta = doc.metadata
                country = meta.get("country", "?")
                org = meta.get("source_org", "?")
                year = meta.get("year", "?")
                topic = meta.get("topic", "?")
                pub = meta.get("publication", "")

                with st.expander(f"#{i} · {country} · {topic} · {org} ({year})", expanded=(i == 1)):
                    cols = st.columns([1, 1, 1, 1])
                    cols[0].markdown(f"**Country:** {country}")
                    cols[1].markdown(f"**Org:** {org}")
                    cols[2].markdown(f"**Year:** {year}")
                    cols[3].markdown(f"**Topic:** `{topic}`")
                    if pub:
                        st.caption(f"Publication: *{pub}*")
                    st.markdown("**Chunk excerpt:**")
                    st.markdown(
                        f'<div style="background:{BG_CODE};border-left:3px solid {GOLD}44;'
                        f'padding:10px 14px;border-radius:0 6px 6px 0;font-size:0.85rem;'
                        f'color:#ccc;white-space:pre-wrap;">{doc.page_content[:500]}…</div>',
                        unsafe_allow_html=True,
                    )

    st.divider()

    # ---- Pydantic schema ---------------------------------------------------
    st.markdown("### Pydantic output schema, `DemographicAnswer`")
    st.caption(
        "When structured mode is enabled in the Chat tab, the LLM is constrained to return "
        "this exact schema via `llm.with_structured_output(DemographicAnswer)`."
    )

    col_schema, col_example = st.columns(2)

    with col_schema:
        st.markdown("**Schema definition** (`rag/pipeline.py`)")
        for field, info in _SCHEMA["fields"].items():
            st.markdown(
                f'<div style="background:{BG_CODE};border:1px solid #333;border-radius:6px;'
                f'padding:8px 12px;margin-bottom:6px;">'
                f'<span style="color:{GOLD};font-weight:600;">{field}</span>'
                f' <span style="color:{TEXT_MUTED};font-size:0.8rem;">{info["type"]}</span><br>'
                f'<span style="color:{TEXT_SUBTLE};font-size:0.8rem;">{info["description"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with col_example:
        st.markdown("**Example output**")
        example = {
            "answer": "Australia's TFR fell to 1.42 in 2022 (ABS, 2022), well below replacement level of 2.1.",
            "key_statistics": ["TFR: 1.42 (ABS, 2022)", "Replacement level: 2.1"],
            "countries_mentioned": ["AUS"],
            "confidence": "high",
            "data_gap": False,
        }
        st.code(json.dumps(example, indent=2), language="json")

    st.divider()

    # ---- Configuration readout --------------------------------------------
    st.markdown("### Index configuration")
    col_a, col_b = st.columns(2)
    with col_a:
        st.json({
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "chunk_size": 512,
            "chunk_overlap": 64,
            "bm25_weight": 0.3,
            "vector_weight": 0.7,
            "top_k": 6,
            "vector_store": "ChromaDB (persistent)",
        })
    with col_b:
        st.json({
            "llm_gateway": "OpenRouter",
            "default_model": "google/gemini-2.5-flash",
            "temperature": 0.2,
            "structured_output": "Pydantic v2 (DemographicAnswer)",
            "eval_framework": "RAGAS v0.2",
            "eval_questions": 20,
        })

    if st.button("Rebuild indices", type="secondary"):
        with st.spinner("Rebuilding…"):
            from rag import build_indices, chunk_documents, load_corpus
            _docs = load_corpus()
            build_indices(chunk_documents(_docs))
            st.cache_resource.clear()
        st.success("Rebuilt. Reload the page to apply.")
