"""Timeline tab — plots demographic metric trends from baked-in corpus metadata.

No LLM call required: metric_years and metric_values are stored directly in each
document's metadata, enabling instant, reliable trend visualisation.
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st
from langchain_core.documents import Document

_TOPIC_LABELS = {
    "fertility": "Fertility",
    "aging": "Population Aging",
    "migration": "Migration",
    "life_expectancy": "Life Expectancy",
    "workforce": "Older Worker Participation",
    "dependency_ratio": "Dependency Ratio",
    "population_projection": "Population Projections",
    "social_cohesion": "Social Cohesion",
    "healthcare": "Healthcare",
    "pension": "Pension Systems",
}

_COUNTRY_COLORS = [
    "#4A90E2", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6",
    "#1ABC9C", "#E67E22", "#34495E", "#E91E63", "#00BCD4",
    "#FF5722", "#8BC34A", "#795548", "#607D8B", "#FF9800",
]


def _get_countries_for_topic(docs: list[Document], topic: str) -> list[str]:
    return sorted({
        d.metadata["country"]
        for d in docs
        if d.metadata.get("topic") == topic and d.metadata.get("metric_years")
    })


def render_timeline_tab(docs: list[Document]) -> None:
    st.header("Trend Timeline")
    st.caption("Explore how demographic indicators have shifted over time across countries. Data is read directly from source metadata — no AI generation.")

    col1, col2 = st.columns([2, 3])

    with col1:
        selected_topic = st.selectbox(
            "Select indicator",
            options=list(_TOPIC_LABELS.keys()),
            format_func=lambda t: _TOPIC_LABELS[t],
        )

        available_countries = _get_countries_for_topic(docs, selected_topic)

        if not available_countries:
            st.warning("No quantitative data available for this indicator.")
            return

        selected_countries = st.multiselect(
            "Select countries",
            options=available_countries,
            default=available_countries[:3],
        )

        plot_btn = st.button("Plot trends", type="primary")

    with col2:
        if not selected_countries:
            st.info("Select at least one country to plot.")
            return

        matched = [
            d for d in docs
            if d.metadata.get("topic") == selected_topic
            and d.metadata.get("country") in selected_countries
            and d.metadata.get("metric_years")
        ]

        if not matched:
            st.warning("No data found for the selected combination.")
            return

        fig = go.Figure()
        metric_label = matched[0].metadata.get("metric_label", "Value")

        for i, doc in enumerate(matched):
            meta = doc.metadata
            years = meta["metric_years"]
            values = meta["metric_values"]
            country = meta["country"]
            color = _COUNTRY_COLORS[i % len(_COUNTRY_COLORS)]

            fig.add_trace(go.Scatter(
                x=years,
                y=values,
                mode="lines+markers",
                name=country,
                line=dict(color=color, width=2),
                marker=dict(size=6),
                hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>{metric_label}: %{{y}}<extra></extra>",
            ))

        fig.update_layout(
            title=f"{_TOPIC_LABELS[selected_topic]} — {metric_label}",
            xaxis_title="Year",
            yaxis_title=metric_label,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e0e0e0"),
            hovermode="x unified",
        )
        fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
        fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Sources**")
        for doc in matched:
            meta = doc.metadata
            st.caption(f"- {meta.get('source_org')} — *{meta.get('publication')}* ({meta.get('year')})")
