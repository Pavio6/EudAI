import tkinter as tk
from tkinter import messagebox, ttk

from services import user_service

SEN_PROFILES = ["general", "dyslexia", "adhd", "autism", "other"]


class RegisterView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.username_var = tk.StringVar()
        self.sen_profile = tk.StringVar(value=SEN_PROFILES[0])
        self._build_widgets()

    def _build_widgets(self) -> None:
        header = tk.Label(self, text="EduAI 注册", font=("Arial", 18))
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

        tk.Label(form, text="支持需求：").grid(row=1, column=0, sticky="w", pady=5)
        self.profile_dropdown = ttk.Combobox(
            form, textvariable=self.sen_profile, values=SEN_PROFILES, state="readonly"
        )
        self.profile_dropdown.grid(row=1, column=1, sticky="ew", pady=5)
        self.profile_dropdown.current(0)

        action_btn = tk.Button(self, text="创建账号", command=self.handle_register, width=20)
        action_btn.pack(pady=(10, 10))

        back_btn = tk.Button(
            self, text="返回登录", command=lambda: self.controller.show_frame("LoginView")
        )
        back_btn.pack()

    def on_show(self) -> None:
        self.username_var.set("")
        self.sen_profile.set(SEN_PROFILES[0])

    def handle_register(self) -> None:
        username = self.username_var.get().strip()
        profile = self.sen_profile.get()
        if not username:
            messagebox.showerror("错误", "用户名不能为空")
            return

        try:
            user_id = user_service.create_user(username, profile)
        except ValueError as exc:
            messagebox.showerror("错误", str(exc))
            return

        messagebox.showinfo("成功", "注册成功")
        login_view = self.controller.frames.get("LoginView")
        if login_view:
            login_view.set_username(username)
        # 登录页或直接登录都可，这里返回登录页
        self.controller.show_frame("LoginView")
