from __future__ import annotations

from typing import Iterable

import ttkbootstrap as ttkb
from ui.theme import CARD_PADDING, PRIMARY


def card(parent: ttkb.Widget, padding=CARD_PADDING, bootstyle=None) -> ttkb.Frame:
    kwargs = {"padding": padding}
    if bootstyle:
        kwargs["bootstyle"] = bootstyle
    return ttkb.Frame(parent, **kwargs)


def section_title(parent: ttkb.Widget, text: str) -> ttkb.Label:
    return ttkb.Label(parent, text=text, style="Emphasis.TLabel")


def brand_panel(
    parent: ttkb.Widget,
    title: str,
    tagline: str,
    bullets: Iterable[str],
    bootstyle=PRIMARY,
) -> ttkb.Frame:
    panel = ttkb.Frame(parent, padding=(24, 24), bootstyle=bootstyle)
    panel.columnconfigure(0, weight=1)

    ttkb.Label(panel, text=title, style="Title.TLabel", bootstyle=f"inverse-{bootstyle}").grid(
        row=0, column=0, sticky="w"
    )
    ttkb.Label(
        panel, text=tagline, style="Subtitle.TLabel", bootstyle=f"inverse-{bootstyle}"
    ).grid(row=1, column=0, sticky="w", pady=(10, 6))

    for idx, bullet in enumerate(bullets):
        ttkb.Label(
            panel,
            text=f"• {bullet}",
            style="Meta.TLabel",
            bootstyle=f"inverse-{bootstyle}",
        ).grid(row=2 + idx, column=0, sticky="w", pady=2)
    return panel


def primary_button(parent: ttkb.Widget, text: str, command=None) -> ttkb.Button:
    return ttkb.Button(parent, text=text, bootstyle=PRIMARY, command=command)


def secondary_button(parent: ttkb.Widget, text: str, command=None) -> ttkb.Button:
    return ttkb.Button(parent, text=text, bootstyle="secondary", command=command)


def danger_button(parent: ttkb.Widget, text: str, command=None) -> ttkb.Button:
    return ttkb.Button(parent, text=text, bootstyle="outline-danger", command=command)
