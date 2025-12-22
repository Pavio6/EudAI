import tkinter as tk
from typing import Dict, Optional

from ui.dashboard_view import DashboardView
from ui.login_view import LoginView
from ui.register_view import RegisterView
from ui.quiz_view import QuizView


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

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames: dict[str, tk.Frame] = {}
        for frame_cls in (LoginView, RegisterView, DashboardView, QuizView):
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


def launch_app() -> None:
    app = App()
    app.mainloop()
