"""Demographic Futures — Streamlit entry point."""
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
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="Demographic Futures",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Global CSS
# ---------------------------------------------------------------------------
_css = (Path(__file__).parent / "styles.css").read_text()
st.markdown(f"<style>{_css}</style>", unsafe_allow_html=True)


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
