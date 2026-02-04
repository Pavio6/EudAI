import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttkb

from services import user_service
from ui.theme import SPACING_16, SPACING_24
from ui.widgets import brand_panel, card, primary_button, secondary_button, section_title

SEN_PROFILES = ["general", "dyslexia", "adhd", "autism", "other"]


class RegisterView(ttkb.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.username_var = tk.StringVar()
        self.sen_profile = tk.StringVar(value=SEN_PROFILES[0])
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
            tagline="Create your profile",
            bullets=[
                "Pick your support needs",
                "Enable accessibility options",
                "Get personalized practice",
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

        header = section_title(inner, "Create account")
        header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, SPACING_16))

        form = ttkb.Frame(inner)
        form.grid(row=1, column=0, columnspan=2, sticky="ew")
        form.columnconfigure(1, weight=1)

        ttkb.Label(form, text="Username").grid(row=0, column=0, sticky="w", pady=6, padx=(0, 10))
        self.username_entry = ttkb.Entry(form, textvariable=self.username_var, width=32)
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=6)

        ttkb.Label(form, text="Support needs").grid(row=1, column=0, sticky="w", pady=6, padx=(0, 10))
        self.profile_dropdown = ttkb.Combobox(
            form, textvariable=self.sen_profile, values=SEN_PROFILES, state="readonly"
        )
        self.profile_dropdown.grid(row=1, column=1, sticky="ew", pady=6)
        self.profile_dropdown.current(0)

        actions = ttkb.Frame(inner)
        actions.grid(row=2, column=0, columnspan=2, pady=(SPACING_16, 0))
        self.create_button = primary_button(actions, "Create account", command=self.handle_register)
        self.create_button.grid(row=0, column=0, padx=(0, 8))
        self.back_button = secondary_button(
            actions, "Back to login", command=lambda: self.controller.show_frame("LoginView")
        )
        self.back_button.grid(row=0, column=1)

    def on_show(self) -> None:
        self.username_var.set("")
        self.sen_profile.set(SEN_PROFILES[0])
        if hasattr(self, "username_entry"):
            self.username_entry.focus_set()

    def handle_register(self) -> None:
        username = self.username_var.get().strip()
        profile = self.sen_profile.get()
        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        try:
            user_id = user_service.create_user(username, profile)
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return

        messagebox.showinfo("Success", "Registered successfully.")
        login_view = self.controller.frames.get("LoginView")
        if login_view:
            login_view.set_username(username)
        # Return to login page after registration
        self.controller.show_frame("LoginView")
