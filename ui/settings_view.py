import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttkb

from services import user_service
from ui.theme import SPACING_16, SPACING_24
from ui.widgets import card, primary_button, secondary_button, section_title


class SettingsView(ttkb.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.tts_enabled = tk.BooleanVar(value=False)
        self.high_contrast = tk.BooleanVar(value=False)
        self._build_widgets()

    def _build_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        shell = ttkb.Frame(self, padding=(SPACING_24, SPACING_24), bootstyle="light")
        shell.grid(row=0, column=0, sticky="nsew")
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(0, weight=1)

        container = card(shell)
        container.grid(row=0, column=0)
        container.columnconfigure(0, weight=1)

        header = section_title(container, "Settings")
        header.grid(row=0, column=0, sticky="w", pady=(0, SPACING_16))
        ttkb.Label(
            container,
            text="Manage accessibility preferences and display options.",
            style="Meta.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(0, SPACING_16))

        form = ttkb.Frame(container)
        form.grid(row=2, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)

        ttkb.Checkbutton(form, text="Enable TTS", variable=self.tts_enabled).grid(
            row=0, column=0, sticky="w", pady=6
        )

        actions = ttkb.Frame(container)
        actions.grid(row=3, column=0, pady=(SPACING_16, 0))
        primary_button(actions, "Save", command=self.handle_save).grid(row=0, column=0, padx=(0, 8))
        secondary_button(
            actions, "Back", command=lambda: self.controller.show_frame("DashboardView")
        ).grid(row=0, column=1)

    def on_show(self) -> None:
        user = getattr(self.controller, "current_user", None)
        if not user:
            messagebox.showerror("Error", "Please sign in first.")
            self.controller.show_frame("LoginView")
            return
        fresh_user = user_service.get_user_by_id(user["user_id"])
        if fresh_user:
            self.controller.set_current_user(fresh_user)
            self.tts_enabled.set(bool(fresh_user.get("tts_enabled", 0)))
            self.high_contrast.set(bool(fresh_user.get("high_contrast", 0)))
            self.controller.apply_theme(self.high_contrast.get())

    def handle_save(self) -> None:
        user = getattr(self.controller, "current_user", None)
        if not user:
            messagebox.showerror("Error", "Please sign in first.")
            self.controller.show_frame("LoginView")
            return

        user_service.update_settings(
            user_id=user["user_id"],
            tts_enabled=self.tts_enabled.get(),
            high_contrast=self.high_contrast.get(),
        )
        updated_user = user_service.get_user_by_id(user["user_id"])
        if updated_user:
            self.controller.set_current_user(updated_user)
            self.controller.apply_theme(bool(updated_user.get("high_contrast", 0)))
        messagebox.showinfo("Saved", "Settings updated successfully.")
