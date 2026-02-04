import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttkb

from services import user_service
from ui.theme import SPACING_16, SPACING_24
from ui.widgets import brand_panel, card, primary_button, secondary_button, section_title


class LoginView(ttkb.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.username_var = tk.StringVar()
        self._build_widgets()

    def _build_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        shell = ttkb.Frame(self, padding=(SPACING_24, SPACING_24), bootstyle="light")
        shell.grid(row=0, column=0, sticky="nsew")

        layout = card(shell, bootstyle="light")
        layout.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)
        layout.columnconfigure(0, weight=1)
        layout.columnconfigure(1, weight=2)

        hero = brand_panel(
            layout,
            title="EduAI",
            tagline="Welcome back",
            bullets=[
                "Personalized learning paths",
                "Track progress with clarity",
                "Support-friendly experience",
            ],
        )
        hero.grid(row=0, column=0, sticky="nsew")

        body = ttkb.Frame(layout, padding=(SPACING_24, SPACING_24))
        body.grid(row=0, column=1, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)
        body.rowconfigure(2, weight=1)

        inner = ttkb.Frame(body)
        inner.grid(row=1, column=0)
        inner.columnconfigure(1, weight=1)

        header = section_title(inner, "Sign in")
        header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, SPACING_16))

        form = ttkb.Frame(inner)
        form.grid(row=1, column=0, columnspan=2, sticky="ew")
        form.columnconfigure(1, weight=1)

        ttkb.Label(form, text="Username").grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
        self.username_entry = ttkb.Entry(form, textvariable=self.username_var, width=32)
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=6)

        actions = ttkb.Frame(inner)
        actions.grid(row=2, column=0, columnspan=2, pady=(SPACING_16, 0))
        self.login_button = primary_button(actions, "Login", command=self.handle_login)
        self.login_button.grid(row=0, column=0, padx=(0, 8))
        self.register_button = secondary_button(
            actions, "Register", command=lambda: self.controller.show_frame("RegisterView")
        )
        self.register_button.grid(row=0, column=1)

    def on_show(self) -> None:
        if not self.username_var.get():
            self.username_var.set("")
        if hasattr(self, "username_entry"):
            self.username_entry.focus_set()

    def set_username(self, username: str) -> None:
        self.username_var.set(username)

    def handle_login(self) -> None:
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return

        user = user_service.get_user_by_username(username)
        if not user:
            messagebox.showerror("Error", "User not found. Please register first.")
            return

        self.controller.set_current_user(user)
        self.controller.show_frame("DashboardView")
