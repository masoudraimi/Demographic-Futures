import streamlit as st
from langchain_core.documents import Document

from palette import BLUE, CONFIDENCE_COLORS, TOPIC_COLORS, TEXT_BODY_ALT

_FLAGS = {
    "Australia": "🇦🇺", "Japan": "🇯🇵", "South Korea": "🇰🇷",
    "Germany": "🇩🇪", "France": "🇫🇷", "United Kingdom": "🇬🇧",
    "Canada": "🇨🇦", "Italy": "🇮🇹", "Sweden": "🇸🇪", "New Zealand": "🇳🇿",
    "Norway": "🇳🇴", "Finland": "🇫🇮", "Spain": "🇪🇸", "Netherlands": "🇳🇱",
    "Switzerland": "🇨🇭", "United States": "🇺🇸", "Greece": "🇬🇷",
    "China": "🇨🇳", "India": "🇮🇳",
}

def _source_card(doc: Document, idx: int) -> None:
    meta = doc.metadata
    country = meta.get("country", "Unknown")
    flag = _FLAGS.get(country, "🌍")
    topic = meta.get("topic", "")
    color = TOPIC_COLORS.get(topic, "#777")
    excerpt = doc.page_content[:200].replace("\n", " ") + "…"

    with st.expander(f"[{idx + 1}] {flag} {country} · {meta.get('year', '?')}"):
        st.caption(f"{meta.get('publication', '')} · **{meta.get('source_org', '')}**")
        st.markdown(
            f'<span style="background:{color};color:white;padding:2px 8px;'
            f'border-radius:12px;font-size:0.72rem">{topic}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f"> {excerpt}")


def _structured_answer_ui(answer_obj, sources: list[Document]) -> None:
    confidence_color = CONFIDENCE_COLORS.get(answer_obj.confidence, "#777")
    st.markdown(answer_obj.answer)

    if answer_obj.key_statistics:
        st.markdown("**Key statistics**")
        chips_html = " ".join(
            f'<span style="background:rgba(74,144,226,0.15);border:1px solid {BLUE};'
            f'color:{TEXT_BODY_ALT};padding:3px 10px;border-radius:14px;font-size:0.78rem;'
            f'margin:2px;display:inline-block">{s}</span>'
            for s in answer_obj.key_statistics
        )
        st.markdown(chips_html, unsafe_allow_html=True)
        st.markdown("")

    st.markdown(
        f'<span style="background:{confidence_color};color:white;padding:3px 10px;'
        f'border-radius:12px;font-size:0.78rem">Confidence: {answer_obj.confidence}</span>',
        unsafe_allow_html=True,
    )
    if answer_obj.data_gap:
        st.warning("Data gap: corpus may not fully cover this question.", icon="⚠️")

    if sources:
        st.markdown("**Sources**")
        for i, doc in enumerate(sources):
            _source_card(doc, i)


def render_chat_tab(retriever) -> None:
    structured_mode = st.toggle(
        "Structured output",
        value=False,
        key="structured_mode_toggle",
        help="Returns grounded statistics, confidence level, and data-gap signal.",
    )

    chain_key = f"chain_{'structured' if structured_mode else 'standard'}"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if chain_key not in st.session_state:
        if structured_mode:
            from rag.pipeline import build_structured_chain
            st.session_state[chain_key] = build_structured_chain(retriever)
        else:
            from rag.pipeline import build_chain_with_sources
            st.session_state[chain_key] = build_chain_with_sources(retriever)

    chain = st.session_state[chain_key]

    if structured_mode:
        st.caption("Structured mode, answer includes statistics and confidence level.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                if not msg.get("structured"):
                    st.markdown("**Sources**")
                    for i, doc in enumerate(msg["sources"]):
                        _source_card(doc, i)

    if prompt := st.chat_input("e.g. How does Australia's fertility rate compare to Japan's?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching corpus…"):
                result = chain.invoke(prompt)
                sources: list[Document] = result["sources"]

            if structured_mode:
                answer_obj = result["answer"]
                _structured_answer_ui(answer_obj, sources)
                answer_text = answer_obj.answer
            else:
                answer_text = result["answer"]
                st.markdown(answer_text)
                if sources:
                    st.markdown("**Sources**")
                    for i, doc in enumerate(sources):
                        _source_card(doc, i)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text,
            "sources": sources,
            "structured": structured_mode,
        })
