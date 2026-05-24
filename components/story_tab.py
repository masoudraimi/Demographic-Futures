"""Story tab — Simon Kuestenmacher-style 7-step demographic narrative.

Each step: one bold headline + one chart + a Simon quote + a planning implication.
Progressive reveal on Step 2 mirrors Simon's live slide-overlay technique.
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

_AGE_BANDS = [
    "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
    "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74",
    "75-79", "80-84", "85+",
]
# Combined male+female (thousands), approx Centre for Population estimates
_POP_2026 = [670, 690, 695, 705, 830, 940, 1010, 985,
             870, 775, 730, 720, 645, 580, 510, 355, 225, 195]
_POP_2036 = [650, 660, 675, 695, 795, 895, 985, 1020,
             985, 940, 860, 755, 725, 680, 625, 445, 320, 315]

# Population scenarios 1901→2120 (millions)
_SCEN = {
    "years_hist": list(range(1901, 2027, 5)),
    "hist": [3.8, 4.0, 4.5, 5.4, 6.6, 6.9, 7.0, 7.5, 8.3, 9.6,
             10.8, 11.6, 12.7, 13.9, 15.2, 16.8, 17.9, 19.2, 20.9, 22.7,
             24.2, 25.1, 26.0, 27.2, 28.0],
    "years_proj": [2026, 2036, 2046, 2056, 2066, 2076, 2086, 2096, 2106, 2116],
    "low":    [28.0, 31.5, 34.5, 37.5, 40.0, 42.5, 44.5, 46.5, 48.0, 49.5],
    "med":    [28.0, 33.0, 37.5, 42.0, 46.5, 51.0, 54.5, 57.0, 58.0, 58.5],
    "high":   [28.0, 35.5, 42.0, 49.0, 56.0, 62.5, 67.5, 71.0, 73.0, 74.5],
}

_USHAPE = {
    "years": [1986, 1991, 1996, 2001, 2006, 2011, 2016, 2021, 2025],
    "uni":   [16,   18,   21,   24,   27,   30,   33,   35,   37],
    "tafe":  [26,   25,   23,   22,   21,   20,   18,   16,   15],
    "low":   [58,   57,   56,   54,   52,   50,   49,   49,   48],
}

_AGED_CARE = {
    "years": [2020, 2025, 2030, 2035, 2040],
    "pop85": [600, 700, 810, 1000, 1200],
    "need":  [324, 378, 437, 540, 648],
    "supply":[230, 255, 285, 320, 360],
}

# Construction cost per sqm (BMT 2025)
_SPRAWL = {
    "types": ["3BR Weatherboard\n(shelf design)", "3BR Brick Veneer\n(shelf design)",
              "4–8 level complex\n(basement parking)", "8+ level complex\n(basement parking)"],
    "costs": [1981, 2351, 3934, 4397],
    "colors": ["#F39C12", "#F39C12", "#E74C3C", "#E74C3C"],
}

# ECI rank + GDP per capita USD (OEC Atlas 2022)
_ECI = {
    "countries": ["Japan", "Germany", "South Korea", "Switzerland", "Sweden",
                  "United States", "Finland", "France", "Netherlands", "United Kingdom",
                  "Italy", "China", "Spain", "New Zealand", "Canada",
                  "Norway", "Greece", "India", "Australia"],
    "rank":      [1,  3,  4,  5,  8, 11, 12, 14, 15, 16,
                  18, 19, 26, 51, 38, 30, 67, 43, 105],
    "gdp_pc":    [33800, 48400, 32400, 92400, 54800, 76400, 50000, 42300, 57800, 45900,
                  35700, 12700, 30100, 46800, 55200, 101900, 20000, 2400, 65400],
}

# ---------------------------------------------------------------------------
# Shared layout
# ---------------------------------------------------------------------------

_L = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e0e0e0", size=12),
)
_G = dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)")


# ---------------------------------------------------------------------------
# Chart builders
# ---------------------------------------------------------------------------

def _chart_age_distribution(show_2036: bool) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=_AGE_BANDS, y=_POP_2026,
        name="2026 (28.0M)",
        marker_color="rgba(150,150,160,0.55)",
        hovertemplate="Age %{x}<br>2026: %{y}K<extra></extra>",
    ))
    if show_2036:
        fig.add_trace(go.Scatter(
            x=_AGE_BANDS, y=_POP_2036,
            name="2036 (31.5M)",
            mode="lines+markers",
            line=dict(color="#00D4FF", width=3),
            marker=dict(size=5),
            hovertemplate="Age %{x}<br>2036: %{y}K<extra></extra>",
        ))
        fig.add_annotation(
            x="40-44", y=985, text="Millennials age into 40s →", showarrow=True,
            arrowhead=2, ax=60, ay=-35, font=dict(color="#00D4FF", size=11),
        )
        fig.add_annotation(
            x="85+", y=315, text="85+ nearly doubles", showarrow=True,
            arrowhead=2, ax=-60, ay=-30, font=dict(color="#E74C3C", size=11),
        )
    fig.update_layout(
        title="Australian population by age — 2026 and 2036 (Centre for Population)",
        xaxis_title="Age band", yaxis_title="Population (thousands)",
        legend=dict(orientation="h", y=1.05),
        **_L,
    )
    fig.update_xaxes(**_G)
    fig.update_yaxes(**_G)
    return fig


def _chart_population_scenarios() -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=_SCEN["years_hist"], y=_SCEN["hist"],
        name="Historical",
        mode="lines", line=dict(color="#E8E8E8", width=2.5),
        hovertemplate="Year %{x}<br>%{y}M<extra>Historical</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=_SCEN["years_proj"], y=_SCEN["low"],
        name="Low (+250K pa)", mode="lines",
        line=dict(color="#4A90E2", width=1.5, dash="dot"),
    ))
    fig.add_trace(go.Scatter(
        x=_SCEN["years_proj"], y=_SCEN["high"],
        name="High (+500K pa)", mode="lines",
        line=dict(color="#E74C3C", width=1.5, dash="dot"),
        fill="tonexty" if False else None,
    ))
    fig.add_trace(go.Scatter(
        x=_SCEN["years_proj"], y=_SCEN["med"],
        name="Medium (+350K pa)", mode="lines+markers",
        line=dict(color="#2ECC71", width=3),
        marker=dict(size=7),
    ))
    # Confidence band
    fig.add_trace(go.Scatter(
        x=_SCEN["years_proj"] + _SCEN["years_proj"][::-1],
        y=_SCEN["high"] + _SCEN["low"][::-1],
        fill="toself", fillcolor="rgba(74,144,226,0.07)",
        line=dict(width=0), showlegend=False, hoverinfo="skip",
    ))
    fig.add_vline(x=2026, line_dash="dash", line_color="rgba(255,255,255,0.3)",
                  annotation_text="Now", annotation_position="top left",
                  annotation_font=dict(color="rgba(255,255,255,0.5)", size=10))
    fig.add_annotation(x=2116, y=58.5, text="56M\n(Simon K.)", showarrow=False,
                       font=dict(color="#F39C12", size=10), xanchor="right")
    fig.update_layout(
        title="Will Australia double in 105, 75, or 53 years? (ABS; low/medium/high scenarios)",
        xaxis_title="Year", yaxis_title="Population (millions)",
        legend=dict(orientation="h", y=1.05),
        **_L,
    )
    fig.update_xaxes(**_G)
    fig.update_yaxes(**_G)
    return fig


def _chart_ushape() -> go.Figure:
    d = _USHAPE
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=d["years"], y=d["uni"],
        name="Skill 1 — University degree",
        mode="lines+markers", stackgroup="one",
        line=dict(color="#4A90E2", width=0),
        fillcolor="rgba(74,144,226,0.7)",
        hovertemplate="Year %{x}<br>Uni: %{y}%<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=d["years"], y=d["tafe"],
        name="Skill 3 — TAFE / trades",
        mode="lines+markers", stackgroup="one",
        line=dict(color="#E74C3C", width=0),
        fillcolor="rgba(231,76,60,0.7)",
        hovertemplate="Year %{x}<br>TAFE: %{y}%<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=d["years"], y=d["low"],
        name="Skill 4–5 — Minimal quals",
        mode="lines+markers", stackgroup="one",
        line=dict(color="#F39C12", width=0),
        fillcolor="rgba(243,156,18,0.4)",
        hovertemplate="Year %{x}<br>Low-skill: %{y}%<extra></extra>",
    ))
    fig.add_annotation(x=2025, y=100, text="Uni: 37%", xanchor="left",
                       showarrow=False, font=dict(color="#4A90E2", size=11))
    fig.add_annotation(x=2025, y=63, text="TAFE: 15%", xanchor="left",
                       showarrow=False, font=dict(color="#E74C3C", size=11))
    fig.update_layout(
        title="Australia transformed into a knowledge economy — Workforce by skill level 1986–2025",
        xaxis_title="Year", yaxis_title="Share of workforce (%)",
        legend=dict(orientation="h", y=1.05),
        **_L,
    )
    fig.update_xaxes(**_G)
    fig.update_yaxes(**_G, range=[0, 100])
    return fig


def _chart_aged_care() -> go.Figure:
    d = _AGED_CARE
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d["years"], y=d["pop85"], name="Population 85+",
                         marker_color="#9B59B6", offsetgroup=0))
    fig.add_trace(go.Bar(x=d["years"], y=d["need"], name="Daily care need (54% of 85+)",
                         marker_color="#E74C3C", offsetgroup=1))
    fig.add_trace(go.Bar(x=d["years"], y=d["supply"], name="Estimated care supply",
                         marker_color="#2ECC71", offsetgroup=2))
    fig.add_annotation(x=2040, y=648, text="Gap: ~290K unmet", showarrow=True,
                       arrowhead=2, ax=-70, ay=-30, font=dict(color="#E74C3C", size=11))
    fig.update_layout(
        title="Australia: 85+ population vs aged care capacity 2020–2040 (AIHW + ABS)",
        xaxis_title="Year", yaxis_title="People (thousands)",
        barmode="group", legend=dict(orientation="h", y=1.05),
        **_L,
    )
    fig.update_xaxes(**_G)
    fig.update_yaxes(**_G)
    return fig


def _chart_sprawl() -> go.Figure:
    d = _SPRAWL
    fig = go.Figure(go.Bar(
        x=d["types"], y=d["costs"],
        marker_color=d["colors"],
        text=[f"${c:,}" for c in d["costs"]],
        textposition="outside",
        textfont=dict(color="#E8E8E8", size=13),
        hovertemplate="%{x}<br><b>$%{y:,}/sqm</b><extra></extra>",
    ))
    fig.add_shape(type="line", x0=-0.5, x1=1.5, y0=2000, y1=2000,
                  line=dict(color="rgba(255,255,255,0.25)", dash="dash"))
    fig.add_annotation(x=0.5, y=2100, text="Suburban range", showarrow=False,
                       font=dict(color="rgba(255,255,255,0.4)", size=10))
    fig.add_shape(type="line", x0=1.5, x1=3.5, y0=4000, y1=4000,
                  line=dict(color="rgba(231,76,60,0.4)", dash="dash"))
    fig.add_annotation(x=2.5, y=4150, text="Density premium", showarrow=False,
                       font=dict(color="#E74C3C", size=10))
    fig.update_layout(
        title="Sprawl is cheaper to build than in-fill housing (BMT Construction Cost Table 2025)",
        xaxis_title="Housing type", yaxis_title="Cost per sqm (AUD)",
        yaxis=dict(range=[0, 5200], **_G),
        **_L,
    )
    fig.update_xaxes(showgrid=False)
    return fig


def _chart_eci() -> go.Figure:
    d = _ECI
    colors = ["#E74C3C" if c == "Australia" else
              "#F39C12" if c == "Norway" else "#4A90E2"
              for c in d["countries"]]
    sizes = [18 if c in ("Australia", "Japan", "Germany", "Norway") else 10
             for c in d["countries"]]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=d["rank"], y=d["gdp_pc"],
        mode="markers+text",
        text=d["countries"],
        textposition=["middle right" if c not in ("Australia", "Norway", "India", "China")
                      else "top center" for c in d["countries"]],
        marker=dict(color=colors, size=sizes, opacity=0.85,
                    line=dict(width=1, color="rgba(255,255,255,0.3)")),
        hovertemplate="<b>%{text}</b><br>ECI rank: %{x}<br>GDP/capita: $%{y:,}<extra></extra>",
    ))
    # Highlight Australia
    aus_idx = d["countries"].index("Australia")
    fig.add_annotation(
        x=d["rank"][aus_idx], y=d["gdp_pc"][aus_idx],
        text="Australia<br>(rank 105)", showarrow=True,
        arrowhead=2, ax=-70, ay=-40,
        font=dict(color="#E74C3C", size=12, weight=700),
        arrowcolor="#E74C3C",
    )
    fig.add_annotation(
        x=50, y=85000,
        text="\"The only reason we are rich is that\nwe have strong institutions.\"",
        showarrow=False, font=dict(color="rgba(200,184,122,0.8)", size=10, style="italic"),
    )
    fig.update_layout(
        title="Economic Complexity Index rank vs GDP per capita — OECD peers + Australia (OEC Atlas 2022)",
        xaxis=dict(title="ECI Rank (1 = most complex)", autorange="reversed", **_G),
        yaxis=dict(title="GDP per capita (USD)", **_G),
        **_L,
    )
    return fig


# ---------------------------------------------------------------------------
# Step content definitions
# ---------------------------------------------------------------------------

_STEPS = [
    {
        "headline": "Australia operates on a very simple business model",
        "quote": "\"She'll be right\" is a grounded observation, not complacency. "
                 "Our four economic pillars remain structurally sound long-term.",
        "planning": "Australia doesn't need to reinvent its economy — but it urgently "
                    "needs to plan for the people and pressures that economy will attract.",
        "chart_fn": None,  # icon grid, handled inline
    },
    {
        "headline": "By 2036 Australia will be bigger, more youthful, and older",
        "quote": "\"Three and a half million new Australians. You shall not be bored. "
                 "But this population growth is not evenly distributed across the age spectrum.\"",
        "planning": "The under-18 cohort barely grows (birth rate declining to ~1.3). "
                    "Almost all growth is imported, aged 18–39. Plan for working-age density, "
                    "not more schools.",
        "chart_fn": "_age_dist",  # special: progressive reveal
    },
    {
        "headline": "Will Australia double in 105, 75, or 53 years?",
        "quote": "\"The children alive today will see Australia at 56 million people. "
                 "And we are planning for this right now.\"",
        "planning": "Whether doubling takes 53 or 105 years, the direction is certain. "
                    "Earmark the Eastern Seaboard fast-rail corridor now — you can't build it yet, "
                    "but the mistake is not planning for it.",
        "chart_fn": _chart_population_scenarios,
    },
    {
        "headline": "Australia transformed into a knowledge economy — but the middle class vanished",
        "quote": "\"This is the opposite of a bell curve. This is the letter U. "
                 "The middle class is small and shrinking, ever less important.\"",
        "planning": "Planning for a bell-curve society no longer works. Rich and poor are "
                    "geographically segregating. Equitable built environments must be designed "
                    "intentionally — they will not emerge from the market.",
        "chart_fn": _chart_ushape,
    },
    {
        "headline": "The aged care cliff — no chance in hell",
        "quote": "\"We are doubling the 85+ cohort in 14 years. We're not importing old people. "
                 "They're already here. Will we double the aged care system? Spoiler: no chance in hell.\"",
        "planning": "Car-dependent communities accelerate mental health decline in older residents. "
                    "The planning lever is building walkable, mixed-use communities so people can "
                    "age in place independently for longer.",
        "chart_fn": _chart_aged_care,
    },
    {
        "headline": "Sprawl is cheaper to build than in-fill housing",
        "quote": "\"All the planning efforts are very much pushing against this hard-core reality "
                 "of building costs. As long as we don't shift the financial model, the wonderful "
                 "attempts to slow down urban sprawl are probably not going to work.\"",
        "planning": "Super funds and sovereign wealth funds are the only long-horizon investors "
                    "who could change the model. Infrastructure costs of sprawl are invisible to "
                    "buyers but surface in government budgets 30 years later.",
        "chart_fn": _chart_sprawl,
    },
    {
        "headline": "Australia ranks 105th in Economic Complexity — and it doesn't matter (yet)",
        "quote": "\"The only reason we are rich is that we have strong institutions distributing "
                 "mining wealth equitably. Anything that weakens those institutions is absolutely dangerous.\"",
        "planning": "Economic complexity predicts long-run adaptability. Australia's rank-105 "
                    "position between Botswana and Ivory Coast is a structural vulnerability disguised "
                    "by resource wealth. Diversification through the knowledge economy is not optional.",
        "chart_fn": _chart_eci,
    },
]


# ---------------------------------------------------------------------------
# Step renderers
# ---------------------------------------------------------------------------

def _render_step_1() -> None:
    pillars = [
        ("⛏️", "Mining", "60 years of global demand remaining. Rare earths super-cycle possible."),
        ("🌾", "Agriculture", "One of the world's few food superpowers. Export value rising with climate stress."),
        ("✈️", "Tourism", "Long-term positive — 4 billion Asian middle-class travellers emerging."),
        ("🎓", "Education", "US PR problems are driving more international students to Australia."),
    ]
    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, pillars):
        col.markdown(
            f"""<div class="glass-card" style="text-align:center;min-height:130px;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="font-weight:700;font-size:1rem;color:#00D4FF;margin:6px 0 4px;">{title}</div>
                <div style="font-size:0.8rem;color:#aaa;">{desc}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """<div style="text-align:center;color:#888;font-size:0.85rem;margin-top:8px;">
        Source: Simon Kuestenmacher, Planning Institute Australia Congress, May 2026
        </div>""",
        unsafe_allow_html=True,
    )


def _render_step_2() -> None:
    show_2036 = st.session_state.get("story_show_2036", False)
    col_btn, _ = st.columns([2, 5])
    with col_btn:
        label = "Hide 2036 overlay" if show_2036 else "Reveal 2036 projection →"
        if st.button(label, key="btn_reveal_2036", type="primary" if not show_2036 else "secondary"):
            st.session_state["story_show_2036"] = not show_2036
            st.rerun()
    st.plotly_chart(_chart_age_distribution(show_2036), use_container_width=True)


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render_story_tab() -> None:
    # Init state
    if "story_step" not in st.session_state:
        st.session_state["story_step"] = 0

    step = st.session_state["story_step"]
    data = _STEPS[step]

    # ---- Header row --------------------------------------------------------
    st.markdown(
        f'<div class="story-headline">{data["headline"]}</div>',
        unsafe_allow_html=True,
    )

    # Step indicator dots
    dots_html = '<div class="step-dots">'
    for i in range(len(_STEPS)):
        cls = "step-dot active" if i == step else "step-dot"
        dots_html += f'<span class="{cls}"></span>'
    dots_html += "</div>"
    st.markdown(dots_html, unsafe_allow_html=True)

    # ---- Quote + planning implication (right column) -----------------------
    main_col, side_col = st.columns([3, 1])

    with side_col:
        st.markdown(
            f'<div class="simon-quote">{data["quote"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="planning-callout"><strong style="color:#00D4FF;">Planning implication</strong><br><br>'
            f'{data["planning"]}</div>',
            unsafe_allow_html=True,
        )

    # ---- Chart area --------------------------------------------------------
    with main_col:
        fn = data["chart_fn"]
        if fn is None:
            _render_step_1()
        elif fn == "_age_dist":
            _render_step_2()
        else:
            st.plotly_chart(fn(), use_container_width=True)

    # ---- Navigation row ----------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    nav_l, nav_mid, nav_r = st.columns([1, 4, 1])

    with nav_l:
        if step > 0:
            if st.button("← Previous", key="btn_prev", use_container_width=True):
                st.session_state["story_step"] = step - 1
                st.session_state.pop("story_show_2036", None)
                st.rerun()

    with nav_mid:
        st.markdown(
            f'<div style="text-align:center;color:#666;font-size:0.82rem;padding-top:8px;">'
            f'Step {step + 1} of {len(_STEPS)} — Australia at 56 Million</div>',
            unsafe_allow_html=True,
        )

    with nav_r:
        if step < len(_STEPS) - 1:
            if st.button("Next →", key="btn_next", use_container_width=True, type="primary"):
                st.session_state["story_step"] = step + 1
                st.session_state.pop("story_show_2036", None)
                st.rerun()
        else:
            st.markdown(
                '<div style="text-align:right;color:#00D4FF;font-size:0.85rem;padding-top:8px;">'
                '✓ End of story</div>',
                unsafe_allow_html=True,
            )

    # ---- Autoplay ----------------------------------------------------------
    with st.expander("Auto-play", expanded=False):
        auto = st.toggle("Advance automatically every 8 seconds", key="story_autoplay")
        if auto and step < len(_STEPS) - 1:
            import time
            time.sleep(8)
            st.session_state["story_step"] = step + 1
            st.session_state.pop("story_show_2036", None)
            st.rerun()
