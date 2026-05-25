"""Citation registry and inline reference popover helper."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

_ROOT = Path(__file__).parent.parent

CITATIONS: dict[str, dict] = {
    "abs_births_2024": {
        "label": "ABS Births, Australia 2024",
        "org": "Australian Bureau of Statistics",
        "file": "data/33010DC01.xlsx",
        "year": 2024,
    },
    "abs_nom_2425": {
        "label": "ABS Overseas Migration 2024-25",
        "org": "Australian Bureau of Statistics",
        "file": "data/34070DO001_202425.xlsx",
        "year": 2025,
    },
    "scanlon_2024": {
        "label": "Mapping Social Cohesion 2024",
        "org": "Scanlon Foundation Research Institute",
        "file": "data/Mapping-Social-Cohesion-2024-Report.pdf",
        "year": 2024,
    },
    "oecd_2026": {
        "label": "OECD Economic Survey: Australia 2026",
        "org": "OECD",
        "file": "data/oecd.pdf",
        "year": 2026,
    },
    "abs_lf_2026": {
        "label": "ABS Labour Force, Australia (Apr 2026)",
        "org": "Australian Bureau of Statistics",
        "file": "data/62020001.xlsx",
        "year": 2026,
    },
    "abs_jobs_2023": {
        "label": "ABS Jobs in Australia 2022-23",
        "org": "Australian Bureau of Statistics",
        "file": (
            "data/Table 1 - Jobs and employment income by sex, age, "
            "business characteristics and geography, 2018-19 to 2022-23.xlsx"
        ),
        "year": 2023,
    },
    "abs_earnings_2025": {
        "label": "ABS Employee Earnings & Hours, May 2025",
        "org": "Australian Bureau of Statistics",
        "file": "data/63060DO001_202505.xlsx",
        "year": 2025,
    },
    "abs_gss_2025": {
        "label": "ABS General Social Survey 2025",
        "org": "Australian Bureau of Statistics",
        "file": "data/GSSDC01.xlsx",
        "year": 2025,
    },
    "oec_hs92_2024": {
        "label": "OEC Country Complexity Rankings 2024 (HS92)",
        "org": "Observatory of Economic Complexity",
        "file": "data/HS92/country-rankings-2024-complexity-20260526091559.csv",
        "year": 2024,
    },
}

_KEYS = list(CITATIONS.keys())
_SUPERSCRIPTS = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "¹⁰", "¹¹", "¹²"]
_CITE_INDEX: dict[str, int] = {k: i for i, k in enumerate(_KEYS)}


def render_cite(key: str, suffix: str = "") -> None:
    """Render a small superscript popover button linked to a source file.

    suffix: unique string per call site to avoid widget key collisions.
    """
    entry = CITATIONS[key]
    sup = _SUPERSCRIPTS[_CITE_INDEX[key]]
    dl_key = f"dl_{key}_{suffix}" if suffix else f"dl_{key}"

    with st.popover(sup, use_container_width=False):
        st.markdown(f"**{entry['label']}**")
        st.caption(f"{entry['org']} · {entry['year']}")
        path = _ROOT / entry["file"]
        if path.exists():
            st.download_button(
                label=f"↓ {path.name}",
                data=path.read_bytes(),
                file_name=path.name,
                key=dl_key,
            )
        else:
            st.caption("*(source file not on disk)*")
