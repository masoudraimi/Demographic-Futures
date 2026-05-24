import streamlit as st
from langchain_core.documents import Document

_FLAGS = {
    "Australia": "🇦🇺", "Japan": "🇯🇵", "South Korea": "🇰🇷",
    "Germany": "🇩🇪", "France": "🇫🇷", "United Kingdom": "🇬🇧",
    "Canada": "🇨🇦", "Italy": "🇮🇹", "Sweden": "🇸🇪", "New Zealand": "🇳🇿",
    "Norway": "🇳🇴", "Finland": "🇫🇮", "Spain": "🇪🇸", "Netherlands": "🇳🇱",
    "Switzerland": "🇨🇭", "United States": "🇺🇸", "Greece": "🇬🇷",
    "China": "🇨🇳", "India": "🇮🇳",
}

_TOPIC_COLORS = {
    "fertility": "#E91E63", "aging": "#9C27B0", "migration": "#2196F3",
    "life_expectancy": "#4CAF50", "workforce": "#FF9800",
    "dependency_ratio": "#F44336", "population_projection": "#00BCD4",
    "social_cohesion": "#8BC34A", "healthcare": "#3F51B5", "pension": "#FF5722",
}


def _source_card(doc: Document, idx: int) -> None:
    meta = doc.metadata
    country = meta.get("country", "Unknown")
    flag = _FLAGS.get(country, "🌍")
    topic = meta.get("topic", "")
    color = _TOPIC_COLORS.get(topic, "#777")
    excerpt = doc.page_content[:280].replace("\n", " ") + "…"

    with st.expander(f"Source {idx + 1}: {flag} {country} — {meta.get('title', '')} ({meta.get('year', '?')})"):
        cols = st.columns([3, 1])
        with cols[0]:
            st.caption(f"*{meta.get('publication', '')}*")
            st.caption(f"**{meta.get('source_org', '')}**")
        with cols[1]:
            st.markdown(
                f'<span style="background:{color};color:white;padding:2px 8px;border-radius:12px;font-size:0.75rem">{topic}</span>',
                unsafe_allow_html=True,
            )
        st.markdown(f"> {excerpt}")


def render_chat_tab(retriever) -> None:
    st.header("Ask about demographic trends")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chain" not in st.session_state:
        from rag.pipeline import build_chain_with_sources
        st.session_state.chain = build_chain_with_sources(retriever)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                st.markdown("**Sources**")
                for i, doc in enumerate(msg["sources"]):
                    _source_card(doc, i)

    if prompt := st.chat_input("e.g. How does Australia's fertility rate compare to Japan's?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching corpus…"):
                result = st.session_state.chain.invoke(prompt)
                answer = result["answer"]
                sources: list[Document] = result["sources"]

            st.markdown(answer)

            if sources:
                st.markdown("**Sources**")
                for i, doc in enumerate(sources):
                    _source_card(doc, i)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": sources}
        )
