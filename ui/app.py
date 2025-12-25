import tkinter as tk
from typing import Dict, Optional

from ui.dashboard_view import DashboardView
from ui.login_view import LoginView
from ui.register_view import RegisterView
from ui.quiz_view import QuizView
from ui.settings_view import SettingsView


class App(tk.Tk):
    """Tkinter application that can switch between frames."""

    def __init__(self) -> None:
        super().__init__()
        self.title("EduAI")
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        target_w = max(800, int(screen_w * 0.6))
        target_h = max(600, int(screen_h * 0.6))
        self.geometry(f"{target_w}x{target_h}")
        self.current_user: Optional[Dict[str, object]] = None
        self.current_user_id: Optional[int] = None
        self.default_bg = self.cget("bg")
        self.default_fg = "#000000"
        self.high_contrast_active = False

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, tk.Frame] = {}
        for frame_cls in (LoginView, RegisterView, DashboardView, QuizView, SettingsView):
            frame = frame_cls(parent=container, controller=self)
            self.frames[frame_cls.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, name: str) -> None:
        frame = self.frames.get(name)
        if not frame:
            raise KeyError(f"No frame named {name}")
        frame.tkraise()
        on_show = getattr(frame, "on_show", None)
        if callable(on_show):
            on_show()

    def set_current_user(self, user: Optional[Dict[str, str]]) -> None:
        self.current_user = user
        self.current_user_id = user.get("user_id") if user else None
        high_contrast = bool(user.get("high_contrast")) if user else False
        self.apply_theme(high_contrast)

    def apply_theme(self, high_contrast: bool) -> None:
        self.high_contrast_active = high_contrast
        colors = {
            "bg": "#111111" if high_contrast else self.default_bg,
            "fg": "#ffffff" if high_contrast else self.default_fg,
            "button_bg": "#f2f2f2" if high_contrast else "SystemButtonFace",
            "button_fg": "#000000",
            "button_active_bg": "#dddddd" if high_contrast else "SystemButtonFace",
            "entry_bg": "#ffffff" if high_contrast else "SystemWindow",
            "entry_fg": "#000000",
        }
        self.configure(bg=colors["bg"])
        for frame in self.frames.values():
            self._set_colors_recursive(frame, colors)

    def _set_colors_recursive(self, widget: tk.Widget, colors: dict) -> None:
        cfg = {}
        if isinstance(widget, tk.Button):
            cfg = {
                "bg": colors["button_bg"],
                "fg": colors["button_fg"],
                "activebackground": colors["button_active_bg"],
                "activeforeground": colors["button_fg"],
            }
        elif isinstance(widget, tk.Entry):
            cfg = {
                "bg": colors["entry_bg"],
                "fg": colors["entry_fg"],
                "insertbackground": colors["entry_fg"],
            }
        else:
            cfg = {"bg": colors["bg"], "fg": colors["fg"]}

        for key, value in cfg.items():
            try:
                widget.configure(**{key: value})
            except tk.TclError:
                continue

        for child in widget.winfo_children():
            self._set_colors_recursive(child, colors)


def launch_app() -> None:
    app = App()
    app.mainloop()
