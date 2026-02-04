from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import ttkbootstrap as ttkb
from ttkbootstrap import Style
from tkinter import font as tkfont

THEME_NAME = "flatly"
HIGH_CONTRAST_THEME = "darkly"

PRIMARY = "primary"
SECONDARY = "secondary"
SUCCESS = "success"
WARNING = "warning"
INFO = "info"
DANGER = "danger"

SPACING_8 = 8
SPACING_12 = 12
SPACING_16 = 16
SPACING_24 = 24

FONT_TITLE = 18
FONT_SUBTITLE = 14
FONT_BODY = 12
FONT_EMPHASIS = 12

CARD_PADDING = (16, 16)
HEADER_HEIGHT = 64

STRIPE_EVEN = "#f7f9fc"
STRIPE_ODD = "#ffffff"

REC_COLORS = {
    "warning": "#b7791f",
    "info": "#2b6cb0",
    "success": "#2f855a",
}


@dataclass(frozen=True)
class ThemeConfig:
    style: Style
    font_family: str


def init_theme() -> ThemeConfig:
    style = ttkb.Style(theme=THEME_NAME)
    base_font = tkfont.nametofont("TkDefaultFont")
    family = base_font.actual("family")

    style.configure(".", font=(family, FONT_BODY))
    style.configure("Title.TLabel", font=(family, FONT_TITLE, "bold"))
    style.configure("Subtitle.TLabel", font=(family, FONT_SUBTITLE))
    style.configure("Emphasis.TLabel", font=(family, FONT_EMPHASIS, "bold"))
    style.configure("Meta.TLabel", font=(family, FONT_BODY))
    style.configure("Treeview", rowheight=28)
    style.configure("Treeview.Heading", font=(family, FONT_BODY, "bold"))
    # Make Labelframe titles and headers readable (deep black).
    style.configure("TLabelframe.Label", font=(family, FONT_BODY, "bold"), foreground="#000000")
    style.configure("Light.TLabelframe.Label", font=(family, FONT_BODY, "bold"), foreground="#000000")
    # Ensure labels on light cards are dark enough.
    style.configure("Meta.TLabel", foreground="#1f2937")
    return ThemeConfig(style=style, font_family=family)


def set_high_contrast(style: Style, enabled: bool) -> None:
    style.theme_use(HIGH_CONTRAST_THEME if enabled else THEME_NAME)
