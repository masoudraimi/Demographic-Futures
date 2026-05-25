"""Demographic Futures — Streamlit entry point."""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

st.set_page_config(
    page_title="Demographic Futures",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Global CSS
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

/* Primary buttons */
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #00D4FF22, #00D4FF44);
    border: 1px solid #00D4FF;
    color: #00D4FF;
}

/* Dividers */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* Glass card */
.glass-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 10px;
    padding: 16px 20px;
}

/* Story section headline */
.story-headline {
    font-size: 1.55rem;
    font-weight: 700;
    color: #E8E8E8;
    letter-spacing: -0.02em;
    line-height: 1.25;
    margin-bottom: 14px;
}

/* Planning implication callout */
.planning-callout {
    background: rgba(0,212,255,0.06);
    border-left: 3px solid #00D4FF;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin-top: 16px;
    font-size: 0.88rem;
    color: #B0C4CE;
    line-height: 1.6;
}

/* Section divider */
.section-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 52px 0 28px;
    color: #555;
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-weight: 600;
}
.section-divider::before,
.section-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #222;
}

/* Expander headers */
[data-testid="stExpander"] summary {
    font-size: 0.92rem;
    color: #888;
    font-weight: 500;
}

/* Body text line-height */
[data-testid="stMarkdownContainer"] p {
    line-height: 1.75;
    color: #C8C8C8;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Load RAG indices (cached)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading corpus and building indices (first run ~10 s)…")
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
# Sidebar — Chat
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div style="padding:8px 0 4px">'
        '<span style="font-size:1.05rem;font-weight:700;color:#E8E8E8">'
        "Ask about demographics</span></div>"
        '<p style="font-size:0.75rem;color:#555;margin:0 0 12px">'
        "Hybrid RAG · BM25 + vector search over 134 corpus entries</p>",
        unsafe_allow_html=True,
    )
    from components.chat_tab import render_chat_tab
    render_chat_tab(retriever)

# ---------------------------------------------------------------------------
# Main page — scrollable dashboard
# ---------------------------------------------------------------------------
from components.dashboard import (
    render_hero,
    render_overview_grid,
    render_section_1,
    render_section_2,
    render_section_3,
    render_section_4,
    render_section_5,
    render_section_6,
    render_section_7,
)

render_hero()
render_overview_grid(docs)
render_section_1()
render_section_2()
render_section_3()
render_section_4()
render_section_5()
render_section_6()
render_section_7()

# ---------------------------------------------------------------------------
# Collapsible appendices
# ---------------------------------------------------------------------------
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

with st.expander("📊  Scenario Projections & Population Pyramids", expanded=False):
    from components.futures_tab import render_futures_tab
    render_futures_tab(docs)

with st.expander("📈  Country Trend Explorer", expanded=False):
    from components.timeline_tab import render_timeline_tab
    render_timeline_tab(docs)

with st.expander("⚙️  Technical: Pipeline & Evaluation", expanded=False):
    tab_p, tab_e = st.tabs(["Pipeline", "Evaluation"])
    with tab_p:
        from components.pipeline_tab import render_pipeline_tab
        render_pipeline_tab(retriever, docs, chunks)
    with tab_e:
        from components.eval_tab import render_eval_tab
        render_eval_tab()
