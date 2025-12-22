import tkinter as tk
from tkinter import messagebox

from services import user_service


class LoginView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.username_var = tk.StringVar()
        self._build_widgets()

    def _build_widgets(self) -> None:
        header = tk.Label(self, text="EduAI 登录", font=("Arial", 18))
        header.pack(pady=(30, 10))

        form_wrapper = tk.Frame(self)
        form_wrapper.pack(expand=True)

        form = tk.Frame(form_wrapper, width=380)
        form.pack(padx=20, pady=10)
        form.pack_propagate(False)
        form.columnconfigure(1, weight=1)

        tk.Label(form, text="用户名：").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(form, textvariable=self.username_var, width=30).grid(
            row=0, column=1, sticky="ew", pady=5
        )

        action_btn = tk.Button(self, text="登录", command=self.handle_login, width=20)
        action_btn.pack(pady=(10, 10))

        register_btn = tk.Button(
            self, text="去注册", command=lambda: self.controller.show_frame("RegisterView")
        )
        register_btn.pack()

    def on_show(self) -> None:
        if not self.username_var.get():
            self.username_var.set("")

    def set_username(self, username: str) -> None:
        self.username_var.set(username)

    def handle_login(self) -> None:
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("错误", "请输入用户名")
            return

        user = user_service.get_user_by_username(username)
        if not user:
            messagebox.showerror("错误", "用户不存在，请注册")
            return

        self.controller.set_current_user(user)
        self.controller.show_frame("DashboardView")
