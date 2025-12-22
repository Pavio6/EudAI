import tkinter as tk
from tkinter import messagebox

from services import user_service


class SettingsView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.tts_enabled = tk.BooleanVar(value=False)
        self.high_contrast = tk.BooleanVar(value=False)
        self._build_widgets()

    def _build_widgets(self) -> None:
        header = tk.Label(self, text="设置", font=("Arial", 18))
        header.pack(pady=(30, 10))

        form = tk.Frame(self)
        form.pack(pady=10, padx=20)
        form.columnconfigure(0, weight=1)

        tk.Checkbutton(form, text="启用 TTS", variable=self.tts_enabled).grid(
            row=0, column=0, sticky="w", pady=5
        )
        tk.Checkbutton(form, text="高对比度模式", variable=self.high_contrast).grid(
            row=1, column=0, sticky="w", pady=5
        )

        actions = tk.Frame(self)
        actions.pack(pady=15)
        tk.Button(actions, text="保存", command=self.handle_save).grid(row=0, column=0, padx=8)
        tk.Button(
            actions, text="返回", command=lambda: self.controller.show_frame("DashboardView")
        ).grid(row=0, column=1, padx=8)

    def on_show(self) -> None:
        user = getattr(self.controller, "current_user", None)
        if not user:
            messagebox.showerror("错误", "请先登录")
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
            messagebox.showerror("错误", "请先登录")
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
        messagebox.showinfo("成功", "保存成功")
