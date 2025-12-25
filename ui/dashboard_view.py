import tkinter as tk
from tkinter import messagebox

from services import progress_service


class DashboardView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self._build_widgets()

    def _build_widgets(self) -> None:
        header = tk.Label(self, text="EduAI Dashboard", font=("Arial", 18))
        header.pack(pady=(30, 10))

        info_frame = tk.Frame(self)
        info_frame.pack(pady=10)

        tk.Label(info_frame, text="Welcome:").grid(row=0, column=0, sticky="e", padx=5)
        self.username_value = tk.Label(info_frame, text="-")
        self.username_value.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(info_frame, text="Support needs:").grid(row=1, column=0, sticky="e", padx=5)
        self.sen_value = tk.Label(info_frame, text="-")
        self.sen_value.grid(row=1, column=1, sticky="w", padx=5)

        stats_frame = tk.LabelFrame(self, text="Progress", padx=10, pady=10)
        stats_frame.pack(pady=10, padx=20, fill="x")
        stats_frame.columnconfigure(1, weight=1)

        tk.Label(stats_frame, text="Total questions:").grid(row=0, column=0, sticky="w", pady=2)
        self.total_attempts_label = tk.Label(stats_frame, text="0")
        self.total_attempts_label.grid(row=0, column=1, sticky="w", pady=2)

        tk.Label(stats_frame, text="Accuracy:").grid(row=1, column=0, sticky="w", pady=2)
        self.accuracy_label = tk.Label(stats_frame, text="0/0 (0%)")
        self.accuracy_label.grid(row=1, column=1, sticky="w", pady=2)

        tk.Label(stats_frame, text="Today:").grid(row=2, column=0, sticky="w", pady=2)
        self.today_attempts_label = tk.Label(stats_frame, text="0")
        self.today_attempts_label.grid(row=2, column=1, sticky="w", pady=2)

        tk.Label(stats_frame, text="Avg time (sec):").grid(row=3, column=0, sticky="w", pady=2)
        self.avg_time_label = tk.Label(stats_frame, text="0")
        self.avg_time_label.grid(row=3, column=1, sticky="w", pady=2)

        tk.Label(stats_frame, text="Last 10: avg difficulty:").grid(row=4, column=0, sticky="w", pady=2)
        self.recent_difficulty_label = tk.Label(stats_frame, text="0")
        self.recent_difficulty_label.grid(row=4, column=1, sticky="w", pady=2)

        tk.Label(stats_frame, text="Last 10: accuracy:").grid(row=5, column=0, sticky="w", pady=2)
        self.recent_accuracy_label = tk.Label(stats_frame, text="0%")
        self.recent_accuracy_label.grid(row=5, column=1, sticky="w", pady=2)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Start quiz", command=self.start_quiz).grid(
            row=0, column=0, padx=10, pady=5
        )
        tk.Button(btn_frame, text="Settings", command=self.open_settings).grid(
            row=0, column=1, padx=10, pady=5
        )
        tk.Button(btn_frame, text="Log out", command=self.logout).grid(
            row=0, column=2, padx=10, pady=5
        )

    def on_show(self) -> None:
        user = getattr(self.controller, "current_user", None)
        if not user:
            self.username_value.config(text="Not signed in")
            self.sen_value.config(text="-")
            self._reset_stats()
            return

        self.username_value.config(text=user.get("username", "-"))
        self.sen_value.config(text=user.get("sen_profile", "-"))
        self._refresh_stats()

    def _reset_stats(self) -> None:
        self.total_attempts_label.config(text="0")
        self.accuracy_label.config(text="0/0 (0%)")
        self.today_attempts_label.config(text="0")
        self.avg_time_label.config(text="0")
        self.recent_difficulty_label.config(text="0")
        self.recent_accuracy_label.config(text="0%")

    def _refresh_stats(self) -> None:
        user_id = getattr(self.controller, "current_user_id", None)
        if not user_id:
            self._reset_stats()
            return

        overall = progress_service.get_overall_stats(user_id)
        today = progress_service.get_today_stats(user_id)
        recent = progress_service.get_recent_stats(user_id)

        total = overall.get("total_attempts", 0) or 0
        correct = overall.get("correct_attempts", 0) or 0
        accuracy_pct = f"{overall.get('accuracy', 0) * 100:.0f}%"
        self.total_attempts_label.config(text=str(total))
        self.accuracy_label.config(text=f"{correct}/{total} ({accuracy_pct})")

        self.today_attempts_label.config(text=str(today.get("today_attempts", 0) or 0))
        avg_time = overall.get("avg_time_spent_sec", 0) or 0
        self.avg_time_label.config(text=f"{avg_time:.1f}")

        self.recent_difficulty_label.config(
            text=f"{(recent.get('recent_avg_difficulty', 0) or 0):.2f}"
        )
        recent_acc_pct = f"{(recent.get('recent_accuracy', 0) or 0) * 100:.0f}%"
        self.recent_accuracy_label.config(text=recent_acc_pct)

    def start_quiz(self) -> None:
        if not getattr(self.controller, "current_user", None):
            messagebox.showerror("Error", "Please sign in first.")
            self.controller.show_frame("LoginView")
            return
        self.controller.show_frame("QuizView")

    def open_settings(self) -> None:
        self.controller.show_frame("SettingsView")

    def logout(self) -> None:
        self.controller.set_current_user(None)
        self.controller.show_frame("LoginView")
