"""Single-page scrollable dashboard — hero, overview grid, and 7 story sections."""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st
from langchain_core.documents import Document

from components.references import render_cite
from components.story_tab import (
    _chart_age_distribution,
    _chart_aged_care,
    _chart_eci,
    _chart_population_scenarios,
    _chart_sprawl,
    _chart_ushape,
    _render_step_1,
)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _divider(label: str) -> None:
    st.markdown(
        f'<div class="section-divider"><span>{label}</span></div>',
        unsafe_allow_html=True,
    )


def _sparkline_fig(years: list, values: list) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=values,
        mode="lines",
        line=dict(color="#00D4FF", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(0,212,255,0.08)",
        hovertemplate="%{x}: %{y:.2f}<extra></extra>",
    ))
    fig.update_layout(
        height=80,
        margin=dict(l=0, r=0, t=4, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def _find_aus_doc(docs: list[Document], topic: str) -> Document | None:
    for doc in docs:
        m = doc.metadata
        if (
            m.get("country") == "Australia"
            and m.get("topic") == topic
            and "metric_years" in m
        ):
            return doc
    return None


def _story_col_header(text: str) -> None:
    st.markdown(
        f'<div class="story-headline">{text}</div>',
        unsafe_allow_html=True,
    )


def _planning_callout(text: str) -> None:
    st.markdown(
        f'<div class="planning-callout">'
        f'<strong style="color:#00D4FF">Planning implication</strong><br><br>'
        f'{text}</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Hero banner
# ---------------------------------------------------------------------------


def render_hero() -> None:
    st.markdown(
        '<div style="padding:32px 0 20px">'
        '<h1 style="font-size:2.6rem;font-weight:800;color:#E8E8E8;margin:0 0 6px;'
        'letter-spacing:-0.03em">Demographic Futures</h1>'
        '<p style="color:#888;font-size:1.05rem;margin:0 0 28px;max-width:640px">'
        "Australia's population, workforce, and economy — from today to 2036 and beyond. "
        "A data-driven look at the structural forces shaping the nation.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    kpis = [
        ("27.2M",  "Population\n(June 2024)",          "abs_births_2024", "hero_pop"),
        ("1.54",   "Total Fertility\nRate (2024)",      "abs_births_2024", "hero_tfr"),
        ("518K",   "Net Overseas\nMigration 2022-23",   "abs_nom_2425",    "hero_nom"),
        ("16.8%",  "Population\naged 65+",              "oecd_2026",       "hero_age"),
        ("#105",   "ECI Rank\n(OEC Atlas 2022)",        None,              ""),
    ]

    cols = st.columns(5)
    for col, (value, label, cite_key, suffix) in zip(cols, kpis):
        with col:
            with st.container(border=True):
                st.markdown(
                    f'<div style="text-align:center;padding:4px 0">'
                    f'<span style="font-size:1.9rem;font-weight:700;color:#00D4FF;display:block">'
                    f"{value}</span>"
                    f'<span style="font-size:0.68rem;color:#888;text-transform:uppercase;'
                    f'letter-spacing:0.08em">{label.replace(chr(10), " ")}</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
                if cite_key:
                    _, mid, _ = st.columns([1, 1, 1])
                    with mid:
                        render_cite(cite_key, suffix)


# ---------------------------------------------------------------------------
# Overview sparkline grid
# ---------------------------------------------------------------------------


def render_overview_grid(docs: list[Document]) -> None:
    _divider("AT A GLANCE — AUSTRALIA")

    grid = [
        ("fertility",           "Total Fertility Rate",              "abs_births_2024", "og_fert"),
        ("aging",               "Population aged 65+ (%)",           "oecd_2026",        "og_age"),
        ("migration",           "Net Overseas Migration",            "abs_nom_2425",     "og_mig"),
        ("life_expectancy",     "Life Expectancy (years)",           "oecd_2026",        "og_le"),
        ("workforce",           "55–74 Labour Participation (%)",    "abs_lf_2026",      "og_work"),
        ("economic_complexity", "ECI Score (lower = less complex)",  None,               ""),
    ]

    for row in [grid[:3], grid[3:]]:
        cols = st.columns(3)
        for col, (topic, label, cite_key, suffix) in zip(cols, row):
            doc = _find_aus_doc(docs, topic)
            with col:
                with st.container(border=True):
                    st.markdown(
                        f'<p style="font-size:0.68rem;color:#888;text-transform:uppercase;'
                        f'letter-spacing:0.08em;margin:0 0 4px">{label}</p>',
                        unsafe_allow_html=True,
                    )
                    if doc:
                        years = doc.metadata.get("metric_years", [])
                        values = doc.metadata.get("metric_values", [])
                        if years and values:
                            latest = values[-1]
                            st.markdown(
                                f'<span style="font-size:1.6rem;font-weight:700;color:#00D4FF">'
                                f"{latest}</span>",
                                unsafe_allow_html=True,
                            )
                            st.plotly_chart(
                                _sparkline_fig(years, values),
                                use_container_width=True,
                                key=f"spark_{topic}",
                            )
                    else:
                        st.caption("No data")
                    if cite_key:
                        render_cite(cite_key, suffix)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Section 1 — Business Model
# ---------------------------------------------------------------------------


def render_section_1() -> None:
    _divider("AUSTRALIA'S BUSINESS MODEL")
    col_chart, col_story = st.columns([55, 45])

    with col_chart:
        _render_step_1()

    with col_story:
        _story_col_header("Australia operates on a very simple business model")
        st.markdown(
            """
Australia's economy rests on **four structural pillars** — mining, agriculture, tourism,
and international education — that have sustained **three decades without a recession**.
No other developed nation matches this record.

> *"She'll be right" is a grounded observation, not complacency. Our four economic
> pillars remain structurally sound long-term."*
> — Simon Kuestenmacher

The question isn't whether this model works today. It's whether Australia is planning
for the **3.5 million new residents** it will add by 2036 — and the infrastructure,
housing, and services they will require.
            """
        )
        _planning_callout(
            "Australia doesn't need to reinvent its economy — but it urgently needs "
            "to plan for the people and pressures that economy will attract."
        )


# ---------------------------------------------------------------------------
# Section 2 — Demographic Shift
# ---------------------------------------------------------------------------


def render_section_2() -> None:
    _divider("DEMOGRAPHIC SHIFT")
    col_chart, col_story = st.columns([55, 45])

    with col_chart:
        show_2036 = st.session_state.get("dash_show_2036", False)
        col_btn, _ = st.columns([2, 3])
        with col_btn:
            label = "Hide 2036 overlay" if show_2036 else "Reveal 2036 projection →"
            if st.button(
                label,
                key="dash_btn_reveal_2036",
                type="primary" if not show_2036 else "secondary",
            ):
                st.session_state["dash_show_2036"] = not show_2036
                st.rerun()
        st.plotly_chart(
            _chart_age_distribution(show_2036),
            use_container_width=True,
            key="dash_age_dist",
        )

    with col_story:
        _story_col_header("By 2036 Australia will be bigger, more youthful, and older")
        st.markdown(
            """
Australia will grow from **28.0M** in 2026 to an estimated **31.5M** by 2036 —
adding **3.5 million people** in a decade. Almost all of that growth is imported:
international migrants aged 18–39.

The under-18 cohort barely grows as the total fertility rate falls toward **1.3** [¹].
Meanwhile the **85+ cohort nearly doubles** — a cohort that requires intensive care
and support, not primary schools.

> *"Three and a half million new Australians. You shall not be bored. But this
> population growth is not evenly distributed across the age spectrum."*
> — Simon Kuestenmacher
            """
        )
        _planning_callout(
            "Almost all growth is working-age and imported. Plan for density in "
            "major cities, not greenfield primary schools."
        )
        st.caption("Sources:")
        c1, _ = st.columns([1, 5])
        with c1:
            render_cite("abs_births_2024", "s2")


# ---------------------------------------------------------------------------
# Section 3 — Population Scenarios
# ---------------------------------------------------------------------------


def render_section_3() -> None:
    _divider("POPULATION SCENARIOS")
    _story_col_header("Will Australia double in 105, 75, or 53 years?")
    st.plotly_chart(
        _chart_population_scenarios(),
        use_container_width=True,
        key="dash_pop_scenarios",
    )

    col_story, _ = st.columns([60, 40])
    with col_story:
        st.markdown(
            """
Australia is on an irreversible growth trajectory. The only uncertainty is *how fast*.
On the **high migration track** (+500K pa), the population doubles in **53 years**.
On the **medium path** (+350K pa), doubling takes **75 years**. On the **low track**
(+250K pa), **105 years**.

> *"The children alive today will see Australia at 56 million people. And we are
> planning for this right now."*
> — Simon Kuestenmacher
            """
        )
        _planning_callout(
            "The direction is certain — only the pace differs. Earmark the Eastern Seaboard "
            "fast-rail corridor now. You can't build it yet, but the mistake is not planning for it."
        )


# ---------------------------------------------------------------------------
# Section 4 — Workforce U-Shape
# ---------------------------------------------------------------------------


def render_section_4() -> None:
    _divider("WORKFORCE & SKILLS")
    col_chart, col_story = st.columns([60, 40])

    with col_chart:
        st.plotly_chart(
            _chart_ushape(),
            use_container_width=True,
            key="dash_ushape",
        )

    with col_story:
        _story_col_header(
            "Australia transformed into a knowledge economy — but the middle class vanished"
        )
        st.markdown(
            """
The share of workers with a university degree rose from **16%** in 1986 to **37%** today [¹].
TAFE and trades shrank from **26%** to **15%**. Low-skill occupations remain stubbornly high.
The workforce now resembles a **U-shape**, not a bell curve.

Total jobs in Australia reached **23.6 million** in 2022-23 [²], with the knowledge
economy anchoring the top and automation and casual work anchoring the base.

> *"This is the opposite of a bell curve. This is the letter U. The middle class is
> small and shrinking, ever less important."*
> — Simon Kuestenmacher
            """
        )
        _planning_callout(
            "Rich and poor are geographically segregating. Equitable built environments "
            "must be designed intentionally — they will not emerge from the market."
        )
        st.caption("Sources:")
        c1, c2, _ = st.columns([1, 1, 4])
        with c1:
            render_cite("abs_lf_2026", "s4")
        with c2:
            render_cite("abs_jobs_2023", "s4")


# ---------------------------------------------------------------------------
# Section 5 — Aged Care Cliff
# ---------------------------------------------------------------------------


def render_section_5() -> None:
    _divider("AGED CARE")
    col_chart, col_story = st.columns([55, 45])

    with col_chart:
        st.plotly_chart(
            _chart_aged_care(),
            use_container_width=True,
            key="dash_aged_care",
        )

    with col_story:
        _story_col_header("The aged care cliff — no chance in hell")
        st.markdown(
            """
Australia's 85+ population will grow from **600,000** in 2020 to **1.2 million** by
2040 — more than doubling in 20 years [¹]. Daily care demand will reach **648,000**.
The system can realistically supply around **360,000** places.

The gap: **~290,000 unmet care needs** by 2040.

> *"We are doubling the 85+ cohort in 14 years. We're not importing old people —
> they're already here. Will we double the aged care system? Spoiler: no chance in hell."*
> — Simon Kuestenmacher
            """
        )
        _planning_callout(
            "Car-dependent communities accelerate mental and physical decline in older residents. "
            "Walkable, mixed-use communities let people age in place independently for longer — "
            "reducing pressure on formal care systems."
        )
        st.caption("Sources:")
        c1, c2, _ = st.columns([1, 1, 4])
        with c1:
            render_cite("abs_births_2024", "s5")
        with c2:
            render_cite("oecd_2026", "s5")


# ---------------------------------------------------------------------------
# Section 6 — Sprawl vs Density
# ---------------------------------------------------------------------------


def render_section_6() -> None:
    _divider("HOUSING & URBAN FORM")
    col_chart, col_story = st.columns([55, 45])

    with col_chart:
        st.plotly_chart(
            _chart_sprawl(),
            use_container_width=True,
            key="dash_sprawl",
        )

    with col_story:
        _story_col_header("Sprawl is cheaper to build than in-fill housing")
        st.markdown(
            """
A 3-bedroom house on the suburban fringe costs **$1,981–$2,351/sqm** to build.
A unit in a mid-to-high-rise complex with basement parking costs **$3,934–$4,397/sqm** —
roughly **double**. As long as this cost gap persists, market forces will keep driving
urban sprawl regardless of planning policy or political will.

> *"All the planning efforts are very much pushing against this hard-core reality of
> building costs. As long as we don't shift the financial model, the wonderful attempts
> to slow down urban sprawl are probably not going to work."*
> — Simon Kuestenmacher
            """
        )
        _planning_callout(
            "Super funds and sovereign wealth funds are the only long-horizon investors who "
            "could change the model. Infrastructure costs of sprawl are invisible to buyers "
            "but surface in government budgets 30 years later."
        )


# ---------------------------------------------------------------------------
# Section 7 — Economic Complexity
# ---------------------------------------------------------------------------


def render_section_7() -> None:
    _divider("ECONOMIC COMPLEXITY")
    col_chart, col_story = st.columns([55, 45])

    with col_chart:
        st.plotly_chart(
            _chart_eci(),
            use_container_width=True,
            key="dash_eci",
        )

    with col_story:
        _story_col_header(
            "Australia ranks 105th in Economic Complexity — and it doesn't matter (yet)"
        )
        st.markdown(
            """
Australia's **ECI rank is 105** out of 133 countries — placing it between Botswana
and the Ivory Coast, despite a GDP per capita of **USD 65,400** [¹]. Japan leads at
rank 1; Germany is 3rd.

The wealth gap is explained by strong institutions distributing mining and resource
revenue equitably across the population. This is **not a permanent advantage**.

> *"The only reason we are rich is that we have strong institutions distributing
> mining wealth equitably. Anything that weakens those institutions is absolutely
> dangerous."*
> — Simon Kuestenmacher
            """
        )
        _planning_callout(
            "If Australia loses institutional quality or commodity prices fall, its rank-105 "
            "complexity offers no buffer. Diversification through the knowledge economy is not "
            "optional — it is a long-run survival question."
        )
        st.caption("Sources:")
        c1, _ = st.columns([1, 5])
        with c1:
            render_cite("oecd_2026", "s7")
