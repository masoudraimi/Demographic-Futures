"""Demographic Futures — Streamlit entry point."""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

st.set_page_config(
    page_title="Demographic Futures",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_resource(show_spinner="Loading corpus and building indices (first run ~10s)…")
def _load():
    from rag import (
        build_indices, build_retriever, chunk_documents, load_corpus, load_indices,
    )
    from rag.index import indices_exist

    docs = load_corpus()
    chunks = chunk_documents(docs)

    if indices_exist():
        chroma, bm25 = load_indices()
    else:
        chroma, bm25 = build_indices(chunks)

    retriever = build_retriever(chroma, bm25)
    return retriever, docs, chunks


retriever, docs, chunks = _load()

tab_chat, tab_timeline, tab_futures, tab_system, tab_eval = st.tabs(
    ["Chat", "Timeline", "Futures", "System", "Evaluation"]
)

with tab_chat:
    from components.chat_tab import render_chat_tab
    structured_mode = st.sidebar.toggle(
        "Structured output",
        value=False,
        help="Returns a typed answer with key statistics, confidence, and data-gap signal.",
    )
    render_chat_tab(retriever, structured_mode=structured_mode)

with tab_timeline:
    from components.timeline_tab import render_timeline_tab
    render_timeline_tab(docs)

with tab_futures:
    from components.futures_tab import render_futures_tab
    render_futures_tab(docs)

with tab_system:
    st.header("System info")

    col1, col2, col3 = st.columns(3)
    col1.metric("Data entries", len(docs))
    col2.metric("Chunks indexed", len(chunks))
    col3.metric("Retriever", "Hybrid BM25 + Chroma")

    topics = sorted({d.metadata.get("topic", "") for d in docs})
    countries = sorted({d.metadata.get("country", "") for d in docs})

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Topics covered**")
        st.write(" · ".join(topics))
    with col_b:
        st.markdown("**Countries covered**")
        st.write(" · ".join(countries))

    st.markdown("---")
    with st.expander("Index configuration"):
        st.json({
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "chunk_size": 512,
            "chunk_overlap": 64,
            "bm25_weight": 0.3,
            "vector_weight": 0.7,
            "top_k": 6,
            "vector_store": "ChromaDB (persistent)",
            "llm_gateway": "OpenRouter",
            "default_model": "google/gemini-flash-1.5",
        })

    st.markdown("---")
    if st.button("Rebuild indices", type="secondary"):
        with st.spinner("Rebuilding…"):
            from rag import build_indices, chunk_documents, load_corpus
            _docs = load_corpus()
            build_indices(chunk_documents(_docs))
            st.cache_resource.clear()
        st.success("Rebuilt. Reload the page to apply.")

with tab_eval:
    from components.eval_tab import render_eval_tab
    render_eval_tab()
