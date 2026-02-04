import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttkb
from ttkbootstrap.constants import PRIMARY

from services import progress_service, recommendation_service, user_service
from ui.theme import SPACING_12, SPACING_16, SPACING_24, STRIPE_EVEN, STRIPE_ODD, REC_COLORS
from ui.widgets import card, danger_button, primary_button, secondary_button, section_title


class DashboardView(ttkb.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self._build_widgets()

    def _build_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        self._build_header()

        separator = ttkb.Separator(self, orient="horizontal")
        separator.grid(row=2, column=0, sticky="ew")

        content = ttkb.Frame(self, bootstyle="light")
        content.grid(row=3, column=0, sticky="nsew")
        content.columnconfigure(0, weight=3, minsize=260)
        content.columnconfigure(1, weight=7)
        content.rowconfigure(0, weight=1)

        self._build_sidebar(content)
        self._build_main(content)
        self._build_footer()

    def _build_header(self) -> None:
        header = ttkb.Frame(self, padding=(SPACING_24, SPACING_16), bootstyle=PRIMARY)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)

        left = ttkb.Frame(header, bootstyle=PRIMARY)
        left.grid(row=0, column=0, sticky="w")
        left.columnconfigure(0, weight=1)

        brand_row = ttkb.Frame(left, bootstyle=PRIMARY)
        brand_row.grid(row=0, column=0, sticky="w")
        self.brand_label = ttkb.Label(
            brand_row, text="EduAI", style="Title.TLabel", bootstyle="inverse-primary"
        )
        self.brand_label.grid(row=0, column=0, sticky="w")
        self.page_label = ttkb.Label(brand_row, text="Dashboard", padding=(8, 2), bootstyle="secondary")
        self.page_label.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.subtitle_label = ttkb.Label(
            left, text="Welcome, -", style="Subtitle.TLabel", bootstyle="inverse-primary"
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.header_tagline = ttkb.Label(
            left, text="Learning Insights Dashboard", style="Meta.TLabel", bootstyle="inverse-primary"
        )
        self.header_tagline.grid(row=2, column=0, sticky="w", pady=(4, 0))

        right = ttkb.Frame(header, bootstyle=PRIMARY)
        right.grid(row=0, column=1, sticky="e")
        right.columnconfigure(0, weight=1)

        self.sen_tag = ttkb.Label(
            right,
            text="Support: -",
            style="Meta.TLabel",
            padding=(8, 3),
            bootstyle="light",
        )
        self.sen_tag.grid(row=0, column=0, sticky="e", pady=(0, 8), padx=(0, 2))

        btns = ttkb.Frame(right, bootstyle=PRIMARY)
        btns.grid(row=1, column=0, sticky="e")
        self.settings_button = secondary_button(btns, "Settings", command=self.open_settings)
        self.settings_button.grid(row=0, column=0, padx=(0, 8))
        self.logout_button = danger_button(btns, "Log out", command=self.logout)
        self.logout_button.grid(row=0, column=1)

        nav = ttkb.Frame(self, padding=(SPACING_24, 6), bootstyle="light")
        nav.grid(row=1, column=0, sticky="ew")
        nav.columnconfigure(0, weight=1)
        nav_left = ttkb.Frame(nav)
        nav_left.grid(row=0, column=0, sticky="w")
        ttkb.Label(nav_left, text="Overview", style="Emphasis.TLabel").grid(row=0, column=0, padx=(0, 16))
        ttkb.Label(nav_left, text="Sessions", style="Emphasis.TLabel").grid(row=0, column=1, padx=(0, 16))
        ttkb.Label(nav_left, text="Recommendations", style="Emphasis.TLabel").grid(row=0, column=2)

    def _build_sidebar(self, parent: ttkb.Frame) -> None:
        sidebar = ttkb.Frame(parent, padding=(SPACING_16, SPACING_16))
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)

        self.progress_card = ttkb.Labelframe(
            sidebar, text="Progress", padding=(SPACING_12, SPACING_12), bootstyle="light"
        )
        self.progress_card.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self.progress_card.columnconfigure(1, weight=1)

        self.total_attempts_label = self._card_row(self.progress_card, 0, "Total questions:")
        self.accuracy_label = self._card_row(self.progress_card, 1, "Accuracy:")
        self.today_attempts_label = self._card_row(self.progress_card, 2, "Today:")
        self.avg_time_label = self._card_row(self.progress_card, 3, "Avg time (sec):")
        self.recent_difficulty_label = self._card_row(self.progress_card, 4, "Last 10 avg difficulty:")
        self.recent_accuracy_label = self._card_row(self.progress_card, 5, "Last 10 accuracy:")

        self.session_card = ttkb.Labelframe(
            sidebar, text="Last Session Summary", padding=(SPACING_12, SPACING_12), bootstyle="light"
        )
        self.session_card.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self.session_card.columnconfigure(1, weight=1)

        self.session_questions_label = self._card_row(self.session_card, 0, "Questions:")
        self.session_accuracy_label = self._card_row(self.session_card, 1, "Accuracy:")
        self.session_avg_time_label = self._card_row(self.session_card, 2, "Avg time (sec):")
        self.session_tts_label = self._card_row(self.session_card, 3, "TTS used:")

        self.tip_card = ttkb.Labelframe(
            sidebar, text="Profile Tip", padding=(SPACING_12, SPACING_12), bootstyle="light"
        )
        self.tip_card.grid(row=2, column=0, sticky="ew")
        self.tip_label = ttkb.Label(self.tip_card, text="—", wraplength=240, style="Meta.TLabel")
        self.tip_label.grid(row=0, column=0, sticky="w")

    def _build_main(self, parent: ttkb.Frame) -> None:
        main = ttkb.Frame(parent, padding=(8, SPACING_16, SPACING_16, SPACING_16))
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        sessions_frame = ttkb.Labelframe(
            main, text="Recent Sessions", padding=(SPACING_12, SPACING_12), bootstyle="light"
        )
        sessions_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        sessions_frame.columnconfigure(0, weight=1)
        sessions_frame.rowconfigure(0, weight=1)

        columns = ("start", "end", "questions", "accuracy", "avg_time")
        self.sessions_table = ttkb.Treeview(
            sessions_frame,
            columns=columns,
            show="headings",
            height=6,
        )
        self.sessions_table.grid(row=0, column=0, sticky="nsew")
        self.sessions_table.heading("start", text="Start")
        self.sessions_table.heading("end", text="End")
        self.sessions_table.heading("questions", text="Questions")
        self.sessions_table.heading("accuracy", text="Accuracy")
        self.sessions_table.heading("avg_time", text="Avg Time")
        self.sessions_table.column("start", width=150, anchor="w", stretch=True)
        self.sessions_table.column("end", width=150, anchor="w", stretch=True)
        self.sessions_table.column("questions", width=90, anchor="center", stretch=False)
        self.sessions_table.column("accuracy", width=90, anchor="center", stretch=False)
        self.sessions_table.column("avg_time", width=90, anchor="center", stretch=False)

        scrollbar = ttkb.Scrollbar(sessions_frame, orient="vertical", command=self.sessions_table.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.sessions_table.configure(yscrollcommand=scrollbar.set)

        rec_frame = ttkb.Labelframe(
            main, text="Recommendations", padding=(SPACING_12, SPACING_12), bootstyle="light"
        )
        rec_frame.grid(row=1, column=0, sticky="nsew")
        rec_frame.columnconfigure(0, weight=1)
        rec_frame.rowconfigure(0, weight=1)

        rec_columns = ("time", "type", "message")
        self.recs_table = ttkb.Treeview(rec_frame, columns=rec_columns, show="headings", height=6)
        self.recs_table.grid(row=0, column=0, sticky="nsew")
        self.recs_table.heading("time", text="Time")
        self.recs_table.heading("type", text="Type")
        self.recs_table.heading("message", text="Message")
        self.recs_table.column("time", width=140, anchor="w", stretch=False)
        self.recs_table.column("type", width=90, anchor="center", stretch=False)
        self.recs_table.column("message", width=400, anchor="w", stretch=True)

        rec_scroll = ttkb.Scrollbar(rec_frame, orient="vertical", command=self.recs_table.yview)
        rec_scroll.grid(row=0, column=1, sticky="ns")
        self.recs_table.configure(yscrollcommand=rec_scroll.set)

        self.rec_empty_label = ttkb.Label(rec_frame, text="No recommendations yet.", style="Meta.TLabel")
        self.rec_empty_label.grid(row=0, column=0, sticky="w", padx=4, pady=4)

    def _build_footer(self) -> None:
        footer = ttkb.Frame(self, padding=(SPACING_16, SPACING_12))
        footer.grid(row=4, column=0, sticky="ew")
        footer.columnconfigure(0, weight=1)

        btns = ttkb.Frame(footer)
        btns.grid(row=0, column=1, sticky="e")
        self.start_button = primary_button(btns, "Start Quiz", command=self.start_quiz)
        self.start_button.grid(row=0, column=0, padx=(0, 8))
        self.footer_settings_button = secondary_button(btns, "Settings", command=self.open_settings)
        self.footer_settings_button.grid(row=0, column=1)

    def _card_row(self, parent: ttkb.Frame, row: int, label: str) -> ttkb.Label:
        ttkb.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=3)
        value = ttkb.Label(parent, text="0")
        value.grid(row=row, column=1, sticky="e", pady=3)
        return value

    def on_show(self) -> None:
        user = getattr(self.controller, "current_user", None)
        if not user:
            self.subtitle_label.config(text="Welcome, -")
            self.sen_tag.config(text="Support: -")
            self.tip_label.config(text="—")
            self._reset_stats()
            return

        self.subtitle_label.config(text=f"Welcome, {user.get('username', '-')}")
        self.sen_tag.config(text=f"Support: {user.get('sen_profile', '-')}")
        self.tip_label.config(text=user_service.get_profile_tip(user.get("sen_profile")))
        self._refresh_stats()

    def _reset_stats(self) -> None:
        self.total_attempts_label.config(text="0")
        self.accuracy_label.config(text="0/0 (0%)")
        self.today_attempts_label.config(text="0")
        self.avg_time_label.config(text="0")
        self.recent_difficulty_label.config(text="0")
        self.recent_accuracy_label.config(text="0%")
        self.session_questions_label.config(text="0")
        self.session_accuracy_label.config(text="0%")
        self.session_avg_time_label.config(text="0")
        self.session_tts_label.config(text="0")
        for item in self.sessions_table.get_children():
            self.sessions_table.delete(item)
        for item in self.recs_table.get_children():
            self.recs_table.delete(item)
        self.rec_empty_label.lift()

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

        last_session = progress_service.get_last_session_summary(user_id)
        session_total = last_session.get("total_attempts", 0) or 0
        session_acc = f"{(last_session.get('accuracy', 0) or 0) * 100:.0f}%"
        session_avg = last_session.get("avg_time_spent_sec", 0) or 0
        session_tts = last_session.get("tts_count", 0) or 0
        self.session_questions_label.config(text=str(session_total))
        self.session_accuracy_label.config(text=session_acc)
        self.session_avg_time_label.config(text=f"{session_avg:.1f}")
        self.session_tts_label.config(text=str(session_tts))

        sessions = progress_service.get_session_list(user_id, limit=5)
        for item in self.sessions_table.get_children():
            self.sessions_table.delete(item)
        for idx, item in enumerate(sessions):
            start = item.get("started_at") or "—"
            end = item.get("ended_at") or "—"
            total = item.get("total_attempts", 0) or 0
            accuracy = f"{(item.get('accuracy', 0) or 0) * 100:.0f}%"
            avg_time = item.get("avg_time_spent_sec")
            avg_time_display = f"{avg_time:.1f}" if isinstance(avg_time, (int, float)) else "—"
            self.sessions_table.insert(
                "",
                "end",
                values=(start, end, total, accuracy, avg_time_display),
                tags=("even" if idx % 2 == 0 else "odd",),
            )
        self._apply_table_stripes(self.sessions_table)

        recs = recommendation_service.get_latest_recommendations(user_id, limit=3)
        for item in self.recs_table.get_children():
            self.recs_table.delete(item)
        if not recs:
            self.rec_empty_label.lift()
        else:
            self.rec_empty_label.lower()
            for idx, rec in enumerate(recs):
                created_at = rec.get("created_at") or "—"
                rec_type = (rec.get("rec_type") or "general").lower()
                rec_value = rec.get("rec_value") or ""
                tag = self._rec_tag_for_type(rec_type)
                self.recs_table.insert(
                    "",
                    "end",
                    values=(created_at, rec_type, rec_value),
                    tags=(tag, "even" if idx % 2 == 0 else "odd"),
                )
        self._apply_table_stripes(self.recs_table)

    def _apply_table_stripes(self, table: ttkb.Treeview) -> None:
        table.tag_configure("even", background=STRIPE_EVEN)
        table.tag_configure("odd", background=STRIPE_ODD)

    def _rec_tag_for_type(self, rec_type: str) -> str:
        mapping = {
            "review": "rec_warning",
            "general": "rec_info",
            "challenge": "rec_success",
            "support": "rec_info",
            "accessibility": "rec_info",
        }
        tag = mapping.get(rec_type, "rec_info")
        self.recs_table.tag_configure("rec_warning", foreground=REC_COLORS["warning"])
        self.recs_table.tag_configure("rec_info", foreground=REC_COLORS["info"])
        self.recs_table.tag_configure("rec_success", foreground=REC_COLORS["success"])
        return tag

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
