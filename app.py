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

# ---------------------------------------------------------------------------
# Global dark-neon CSS (ColdMath-inspired)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* Base */
html, body, [data-testid="stApp"] {
    background-color: #0d0d0d;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,212,255,0.35);
    border-radius: 8px;
    padding: 12px 16px;
    box-shadow: 0 0 10px rgba(0,212,255,0.12);
}
[data-testid="stMetricValue"] { color: #00D4FF; }
[data-testid="stMetricDelta"] { font-size: 0.8rem; }

/* Tabs */
[data-testid="stTabs"] button {
    font-weight: 600;
    letter-spacing: 0.03em;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #00D4FF;
    border-bottom: 2px solid #00D4FF;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0a0a0a;
    border-right: 1px solid rgba(0,212,255,0.15);
}

/* Info/callout boxes */
[data-testid="stInfo"] {
    background: rgba(0,212,255,0.06);
    border-left: 3px solid #00D4FF;
}

/* Buttons */
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #00D4FF22, #00D4FF44);
    border: 1px solid #00D4FF;
    color: #00D4FF;
}

/* Dividers */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}

/* Glass card helper — apply via st.markdown unsafe_allow_html */
.glass-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 10px;
    padding: 16px 20px;
}

/* Story step headline */
.story-headline {
    font-size: 1.6rem;
    font-weight: 700;
    color: #E8E8E8;
    letter-spacing: -0.02em;
    line-height: 1.25;
    margin-bottom: 4px;
}

/* Planning implication callout */
.planning-callout {
    background: rgba(0,212,255,0.06);
    border-left: 3px solid #00D4FF;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-top: 12px;
    font-size: 0.88rem;
    color: #B0C4CE;
}

/* Quote block */
.simon-quote {
    border-left: 3px solid rgba(255,200,0,0.5);
    padding: 8px 14px;
    margin: 10px 0;
    font-style: italic;
    color: #C8B87A;
    font-size: 0.9rem;
}

/* Step indicator dots */
.step-dots {
    display: flex; gap: 6px; justify-content: center;
    margin: 8px 0;
}
.step-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: rgba(255,255,255,0.2);
    display: inline-block;
}
.step-dot.active { background: #00D4FF; box-shadow: 0 0 6px #00D4FF; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Load RAG indices (cached)
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_story, tab_chat, tab_timeline, tab_futures, tab_pipeline, tab_eval = st.tabs(
    ["Story", "Chat", "Timeline", "Futures", "Pipeline", "Evaluation"]
)

with tab_story:
    from components.story_tab import render_story_tab
    render_story_tab()

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

with tab_pipeline:
    from components.pipeline_tab import render_pipeline_tab
    render_pipeline_tab(retriever, docs, chunks)

with tab_eval:
    from components.eval_tab import render_eval_tab
    render_eval_tab()
