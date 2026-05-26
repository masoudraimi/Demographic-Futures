"""Futures tab, scenario-planning visualisations inspired by Simon Kuestenmacher's
PIA Congress 2026 keynote. No LLM calls: all data is baked in.
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st
from langchain_core.documents import Document

from palette import BLUE, BLUE_3DB, GREEN, MIGRATION_COLORS, ORANGE, PINK, PURPLE, RED, TEXT_BODY_ALT

# ---------------------------------------------------------------------------
# Hardcoded scenario data (sourced from ABS 3222.0, AIHW, ABS 6291.0, IGR 2023)
# ---------------------------------------------------------------------------

_POP_SCENARIOS = {
    "years": [2022, 2031, 2041, 2051, 2061, 2071],
    "series_a": [25.9, 30.5, 35.7, 41.3, 47.4, 54.8],   # high: sustained high NOM
    "series_b": [25.9, 28.7, 31.5, 34.3, 37.0, 39.9],   # base
    "series_c": [25.9, 27.3, 28.8, 30.1, 31.5, 32.7],   # low
}

_USHAPE = {
    "years": [1986, 1996, 2006, 2016, 2023, 2036],
    "skill_l1_uni": [16, 21, 27, 33, 37, 43],          # uni degree (%)
    "skill_l3_tafe": [26, 23, 21, 18, 15, 12],          # TAFE / trades (%)
    "skill_l45_low": [36, 38, 40, 43, 48, 45],          # minimal quals (%)
}

_AGED_CARE = {
    "years": [2020, 2025, 2030, 2035, 2040],
    "pop_85plus": [600, 700, 810, 1000, 1200],           # 85+ population (000s)
    "daily_care_need": [324, 378, 437, 540, 648],        # 54% needing daily care (000s)
    "care_supply": [230, 255, 285, 320, 360],            # estimated supply (000s)
}

_MIGRATION_COMP = {
    "years": [2006, 2009, 2012, 2015, 2018, 2019, 2021, 2023],
    "skilled":      [72,  85,  90,  93, 108, 109,  95, 195],
    "student":      [42,  55,  65,  75,  90,  90, -60, 190],
    "family":       [35,  38,  42,  48,  53,  55,  50,  85],
    "humanitarian": [ 9,  12,  13,  14,  16,  18,  15,  18],
}

_PYRAMID_2022 = {
    "bands": ["0-4","5-9","10-14","15-19","20-24","25-29","30-34","35-39",
              "40-44","45-49","50-54","55-59","60-64","65-69","70-74",
              "75-79","80-84","85+"],
    "male":   [778,  789,  789,  777,  855,  945,  965,  948,
               882,  841,  812,  793,  687,  628,  573,
               399,  250,  200],
    "female": [742,  751,  751,  743,  825,  925,  955,  942,
               878,  839,  808,  797,  693,  642,  607,
               451,  310,  330],
}

_PYRAMID_2036 = {
    "bands": _PYRAMID_2022["bands"],
    "male":   [740,  760,  790,  790,  830,  910,  960,  990,
               975,  958,  945,  865,  840,  800,  730,
               620,  420,  310],
    "female": [705,  725,  752,  752,  792,  875,  945,  978,
               960,  945,  930,  858,  840,  805,  740,
               650,  470,  430],
}


# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------

_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_BODY_ALT),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
_GRID = dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")


def _pop_scenarios_chart() -> go.Figure:
    d = _POP_SCENARIOS
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=d["years"], y=d["series_a"], name="Series A, High",
        mode="lines", line=dict(color=RED, width=1.5, dash="dot"),
    ))
    fig.add_trace(go.Scatter(
        x=d["years"], y=d["series_c"], name="Series C, Low",
        fill=None, mode="lines", line=dict(color=BLUE_3DB, width=1.5, dash="dot"),
    ))
    fig.add_trace(go.Scatter(
        x=d["years"], y=d["series_a"],
        fill="tonexty", fillcolor="rgba(231,76,60,0.08)",
        line=dict(width=0), showlegend=False, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=d["years"], y=d["series_b"], name="Series B, Base",
        mode="lines+markers", line=dict(color=GREEN, width=3),
        marker=dict(size=7),
        hovertemplate="Year: %{x}<br>Population: %{y}M<extra>Series B</extra>",
    ))

    fig.add_annotation(x=2022, y=25.9, text="Today: 26M", showarrow=True,
                       arrowhead=2, ax=40, ay=-30, font=dict(color=TEXT_BODY_ALT, size=11))
    fig.add_annotation(x=2071, y=39.9, text="~40M (base)", showarrow=False,
                       font=dict(color=GREEN, size=11))
    fig.add_hline(y=56, line_dash="dash", line_color="rgba(255,255,255,0.3)",
                  annotation_text="56M, Simon Kuestenmacher estimate",
                  annotation_position="bottom right",
                  annotation_font=dict(color="rgba(255,255,255,0.5)", size=10))

    fig.update_layout(
        title="Australia Population Scenarios 2022–2071 (ABS Series A/B/C)",
        xaxis_title="Year", yaxis_title="Population (millions)",
        **_LAYOUT,
    )
    fig.update_xaxes(**_GRID)
    fig.update_yaxes(**_GRID)
    return fig


def _ushape_chart() -> go.Figure:
    d = _USHAPE
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=d["years"], y=d["skill_l1_uni"], name="Skill Level 1, University degree",
        marker_color=BLUE, offsetgroup=0,
    ))
    fig.add_trace(go.Bar(
        x=d["years"], y=d["skill_l3_tafe"], name="Skill Level 3, TAFE / trades",
        marker_color=RED, offsetgroup=1,
    ))
    fig.add_trace(go.Scatter(
        x=d["years"], y=d["skill_l45_low"],
        name="Skill Level 4+5, Minimal quals",
        mode="lines+markers", line=dict(color=ORANGE, width=2.5),
        marker=dict(size=7), yaxis="y2",
    ))

    fig.add_annotation(
        x=2023, y=15, text="TAFE: 15%", showarrow=True,
        arrowhead=2, ax=-50, ay=20, font=dict(color=RED, size=11),
    )
    fig.add_annotation(
        x=2023, y=37, text="Uni: 37%", showarrow=True,
        arrowhead=2, ax=50, ay=-20, font=dict(color=BLUE, size=11),
    )

    fig.update_layout(
        title="Australia's U-Shaped Workforce, Skill Level Distribution 1986–2036",
        xaxis_title="Year",
        yaxis=dict(title="Share of jobs (%)", **_GRID, color=TEXT_BODY_ALT),
        yaxis2=dict(title="Skill 4+5 combined (%)", overlaying="y", side="right",
                    showgrid=False, color=ORANGE),
        barmode="group",
        **_LAYOUT,
    )
    return fig


def _aged_care_chart() -> go.Figure:
    d = _AGED_CARE
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=d["years"], y=d["pop_85plus"], name="Population 85+",
        marker_color=PURPLE, offsetgroup=0,
    ))
    fig.add_trace(go.Bar(
        x=d["years"], y=d["daily_care_need"], name="Daily care need (54% of 85+)",
        marker_color=RED, offsetgroup=1,
    ))
    fig.add_trace(go.Bar(
        x=d["years"], y=d["care_supply"], name="Estimated care supply",
        marker_color=GREEN, offsetgroup=2,
    ))

    fig.add_annotation(x=2040, y=648, text="Gap: ~290K unmet", showarrow=True,
                       arrowhead=2, ax=-70, ay=-30, font=dict(color=RED, size=11))

    fig.update_layout(
        title="Australia: 85+ Population vs Aged Care Capacity 2020–2040",
        xaxis_title="Year", yaxis_title="People (thousands)",
        barmode="group",
        **_LAYOUT,
    )
    fig.update_xaxes(**_GRID)
    fig.update_yaxes(**_GRID)
    return fig


def _migration_comp_chart() -> go.Figure:
    d = _MIGRATION_COMP
    fig = go.Figure()

    colors = MIGRATION_COLORS
    labels = {"skilled": "Skilled", "student": "Student / temporary",
              "family": "Family", "humanitarian": "Humanitarian"}

    for key in ("skilled", "student", "family", "humanitarian"):
        fig.add_trace(go.Scatter(
            x=d["years"], y=d[key],
            name=labels[key],
            mode="lines",
            stackgroup="one",
            line=dict(color=colors[key], width=0.5),
            fillcolor=colors[key].replace(")", ",0.6)").replace("rgb", "rgba")
                if colors[key].startswith("rgb") else colors[key],
            hovertemplate=f"<b>{labels[key]}</b><br>Year: %{{x}}<br>NOM: %{{y}}K<extra></extra>",
        ))

    fig.add_annotation(x=2021, y=-40, text="COVID-19\nborder closures", showarrow=True,
                       arrowhead=2, ax=50, ay=-40, font=dict(color="rgba(255,255,255,0.7)", size=10))

    fig.update_layout(
        title="Australia: Net Overseas Migration by Visa Type 2006–2023",
        xaxis_title="Year", yaxis_title="NOM (thousands)",
        **_LAYOUT,
    )
    fig.update_xaxes(**_GRID)
    fig.update_yaxes(**_GRID)
    return fig


def _pyramid_chart(year: str) -> go.Figure:
    data = _PYRAMID_2022 if year == "2022" else _PYRAMID_2036
    bands = data["bands"]
    males = [-v for v in data["male"]]   # negative for left side
    females = data["female"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=bands, x=males, name="Male",
        orientation="h", marker_color=BLUE,
        hovertemplate="<b>Male</b> %{y}<br>%{customdata:,}K<extra></extra>",
        customdata=data["male"],
    ))
    fig.add_trace(go.Bar(
        y=bands, x=females, name="Female",
        orientation="h", marker_color=PINK,
        hovertemplate="<b>Female</b> %{y}<br>%{x:,}K<extra></extra>",
    ))

    fig.update_layout(
        title=f"Australia Population Pyramid, {year}",
        barmode="overlay",
        xaxis=dict(
            title="Population (thousands)",
            tickvals=[-1500, -1000, -500, 0, 500, 1000, 1500],
            ticktext=["1500", "1000", "500", "0", "500", "1000", "1500"],
            **_GRID,
        ),
        yaxis=dict(title="Age band", **_GRID),
        **_LAYOUT,
    )
    return fig


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render_futures_tab(docs: list[Document]) -> None:
    st.header("Population Futures")
    st.caption(
        "Scenario-planning visualisations drawn from ABS, AIHW, Treasury, and independent "
        "demographic analysis. No AI generation, data is sourced directly."
    )

    # ---- A: Population Scenarios ----------------------------------------
    st.subheader("A · How many Australians by 2071?")
    st.caption(
        "ABS Series A/B/C projections. The primary uncertainty is migration, not fertility. "
        "Simon Kuestenmacher's 56M estimate (dashed line) assumes sustained high-migration trajectories."
    )
    st.plotly_chart(_pop_scenarios_chart(), use_container_width=True)

    st.divider()

    # ---- B: U-Shape Workforce -------------------------------------------
    st.subheader("B · The U-Shaped Society, Workforce Skill Distribution")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(_ushape_chart(), use_container_width=True)
    with col2:
        st.markdown("**The bell curve is gone.**")
        st.markdown(
            "- University-qualified jobs: **37%** and rising\n"
            "- TAFE/trades backbone: down to **15%**\n"
            "- Minimal qualification jobs: **48%** combined\n\n"
            "The 'dumbest place in the market' is targeting the middle, it no longer exists."
        )

    st.divider()

    # ---- C: Aged Care Gap -----------------------------------------------
    st.subheader("C · The 85+ Aged Care Crisis")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(_aged_care_chart(), use_container_width=True)
    with col2:
        st.markdown("**Structurally impossible by 2040.**")
        st.markdown(
            "- 85+ population doubles: 600K → 1.2M\n"
            "- 54% require daily care → 648K people\n"
            "- Current supply: ~320K places\n"
            "- Gap: **~290,000 unmet** by 2040\n\n"
            "The system cannot scale fast enough under current planning. "
            "Community-embedded aging-in-place is the only viable path."
        )

    st.divider()

    # ---- D: Migration Composition ----------------------------------------
    st.subheader("D · Migration Is Not Monolithic, Composition of NOM 2006–2023")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(_migration_comp_chart(), use_container_width=True)
    with col2:
        st.markdown("**NOM = 518K in 2022-23, a record.**")
        st.markdown(
            "- ~40% are international students, highly volatile\n"
            "- Skilled migrants: net +$330K lifetime fiscal value\n"
            "- COVID closed the tap; post-COVID surge masks structural composition\n"
            "- 900K students in workforce data need discounting\n\n"
            "Source: ABS Migration, Australia 2022-23 (Cat. 3412.0)"
        )

    st.divider()

    # ---- E: Population Pyramid ------------------------------------------
    st.subheader("E · Population Pyramid, The Inverting Triangle")
    year = st.radio("Select year", ["2022", "2036"], horizontal=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(_pyramid_chart(year), use_container_width=True)
    with col2:
        if year == "2022":
            st.markdown("**2022, The baby boomer bulge is in the 55-70 band.**")
            st.markdown(
                "- Wide base of working-age millennials\n"
                "- 85+ cohort: 530K (small but doubling)\n"
                "- Classic bulge shape from 1960s baby boom\n\n"
                "Source: ABS Estimated Resident Population (Cat. 3101.0)"
            )
        else:
            st.markdown("**2036, The top is expanding fast.**")
            st.markdown(
                "- 60-74 band swells dramatically\n"
                "- 85+ cohort approaches 740K\n"
                "- Narrowing base from sub-replacement fertility\n\n"
                "The triangle is inverting. This underpins every aged care, "
                "pension, and healthcare fiscal projection through the 2030s."
            )
