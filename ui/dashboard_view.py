import tkinter as tk
from tkinter import messagebox


class DashboardView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self._build_widgets()

    def _build_widgets(self) -> None:
        header = tk.Label(self, text="Dashboard", font=("Arial", 18))
        header.pack(pady=(30, 10))

        info_frame = tk.Frame(self)
        info_frame.pack(pady=10)

        tk.Label(info_frame, text="欢迎：").grid(row=0, column=0, sticky="e", padx=5)
        self.username_value = tk.Label(info_frame, text="-")
        self.username_value.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(info_frame, text="支持需求：").grid(row=1, column=0, sticky="e", padx=5)
        self.sen_value = tk.Label(info_frame, text="-")
        self.sen_value.grid(row=1, column=1, sticky="w", padx=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="开始测验", command=self.start_quiz).grid(
            row=0, column=0, padx=10, pady=5
        )
        tk.Button(btn_frame, text="设置", command=self.open_settings).grid(
            row=0, column=1, padx=10, pady=5
        )
        tk.Button(btn_frame, text="退出登录", command=self.logout).grid(
            row=0, column=2, padx=10, pady=5
        )

    def on_show(self) -> None:
        user = getattr(self.controller, "current_user", None)
        if not user:
            self.username_value.config(text="未登录")
            self.sen_value.config(text="-")
            return

        self.username_value.config(text=user.get("username", "-"))
        self.sen_value.config(text=user.get("sen_profile", "-"))

    def start_quiz(self) -> None:
        if not getattr(self.controller, "current_user", None):
            messagebox.showerror("错误", "请先登录")
            self.controller.show_frame("LoginView")
            return
        self.controller.show_frame("QuizView")

    def open_settings(self) -> None:
        messagebox.showinfo("设置", "Coming soon")

    def logout(self) -> None:
        self.controller.set_current_user(None)
        self.controller.show_frame("LoginView")
