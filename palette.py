"""Central colour palette for Demographic Futures.

All hex codes and colour decisions live here. Every other file imports
from this module, no bare hex strings anywhere else.

CSS custom properties are injected into :root {} by app.py at startup,
so styles.css can reference them as var(--gold) etc.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Brand accents, Australian national colours
# ---------------------------------------------------------------------------
GOLD      = "#FAB713"        # Pantone 116 C, wattle / national sporting colour
GOLD_RGB  = "250,183,19"      # bare R,G,B for rgba() inside CSS and Python

AUS_GREEN     = "#00853E"    # Pantone 348 C, eucalyptus / national sporting colour
AUS_GREEN_RGB = "0,133,62"

# ---------------------------------------------------------------------------
# Surfaces & structure
# ---------------------------------------------------------------------------
BG_PAGE    = "#0d0d0d"
BG_SIDEBAR = "#0a0a0a"
BG_CODE    = "#141414"
DIVIDER    = "#222"

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
TEXT_HEADING  = "#E8E8E8"
TEXT_BODY     = "#C8C8C8"
TEXT_BODY_ALT = "#e0e0e0"   # used in chart font dicts
TEXT_MUTED    = "#888"
TEXT_SUBTLE   = "#aaa"
TEXT_DIM      = "#666"
TEXT_CALLOUT  = "#C8B87A"   # warm sandy gold for planning-callout body

# ---------------------------------------------------------------------------
# Semantic chart / data colours
# ---------------------------------------------------------------------------
RED          = "#E74C3C"
GREEN        = "#2ECC71"
ORANGE       = "#F39C12"
BLUE         = "#4A90E2"
PURPLE       = "#9B59B6"
PINK         = "#E91E63"
TEAL         = "#1ABC9C"
DARK_ORANGE  = "#E67E22"
SLATE        = "#34495E"
LIME         = "#8BC34A"
BROWN        = "#795548"
GRAY_BLUE    = "#607D8B"
LIGHT_ORANGE = "#FF9800"
FIRE         = "#FF5722"
CYAN         = "#00BCD4"
BLUE_3DB     = "#3498DB"    # futures_tab scenario line

# Material-style colours used in chat_tab topic chips
M_PURPLE = "#9C27B0"
M_BLUE   = "#2196F3"
M_GREEN  = "#4CAF50"
M_RED    = "#F44336"
M_INDIGO = "#3F51B5"

# Eval-tab ablation chart trio
EVAL_INDIGO     = "#5C6BC0"
EVAL_LIGHT_BLUE = "#42A5F5"

# ---------------------------------------------------------------------------
# Structured lookups (imported directly by component modules)
# ---------------------------------------------------------------------------

TOPIC_COLORS: dict[str, str] = {
    "fertility":            PINK,
    "aging":                M_PURPLE,
    "migration":            M_BLUE,
    "life_expectancy":      M_GREEN,
    "workforce":            LIGHT_ORANGE,
    "dependency_ratio":     M_RED,
    "population_projection": GOLD,
    "social_cohesion":      LIME,
    "healthcare":           M_INDIGO,
    "pension":              FIRE,
}

CONFIDENCE_COLORS: dict[str, str] = {
    "high":   GREEN,
    "medium": ORANGE,
    "low":    RED,
}

COUNTRY_COLORS: list[str] = [
    BLUE, RED, GREEN, ORANGE, PURPLE,
    TEAL, DARK_ORANGE, SLATE, PINK, CYAN,
    FIRE, LIME, BROWN, GRAY_BLUE, LIGHT_ORANGE,
]

MIGRATION_COLORS: dict[str, str] = {
    "skilled":      BLUE,
    "student":      GREEN,
    "family":       ORANGE,
    "humanitarian": PURPLE,
}

# ---------------------------------------------------------------------------
# CSS custom-property map, injected into :root {} by app.py
# ---------------------------------------------------------------------------
CSS_VARS: dict[str, str] = {
    "--gold":           GOLD,
    "--gold-rgb":       GOLD_RGB,
    "--aus-green":      AUS_GREEN,
    "--aus-green-rgb":  AUS_GREEN_RGB,
    "--bg-page":        BG_PAGE,
    "--bg-sidebar":     BG_SIDEBAR,
    "--bg-code":        BG_CODE,
    "--divider":        DIVIDER,
    "--text-heading":   TEXT_HEADING,
    "--text-body":      TEXT_BODY,
    "--text-body-alt":  TEXT_BODY_ALT,
    "--text-muted":     TEXT_MUTED,
    "--text-subtle":    TEXT_SUBTLE,
    "--text-dim":       TEXT_DIM,
    "--text-callout":   TEXT_CALLOUT,
    "--chart-red":      RED,
    "--chart-green":    GREEN,
    "--chart-orange":   ORANGE,
    "--chart-blue":     BLUE,
    "--chart-purple":   PURPLE,
    "--chart-pink":     PINK,
}
