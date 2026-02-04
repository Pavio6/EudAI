import time
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttkb

from models.recommender import next_difficulty
from services import progress_service, quiz_service, recommendation_service, tts_service, user_service
from ui.theme import SPACING_12, SPACING_16, SPACING_24
from ui.widgets import card, primary_button, secondary_button, section_title


class QuizView(ttkb.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.subject = "Math"
        self.current_difficulty = 1
        self.seen_question_ids: set[int] = set()
        self.current_question: dict | None = None
        self.session_id: int | None = None
        self.question_start_time: float = 0.0
        self.used_tts_for_question = False
        self.answer_locked = False
        self.correct_streak = 0
        self.session_attempts = 0
        self.session_correct = 0
        self.session_time_sum = 0
        self.session_tts_count = 0
        self._build_widgets()

    def _build_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        shell = ttkb.Frame(self, padding=(SPACING_24, SPACING_24), bootstyle="light")
        shell.grid(row=0, column=0, sticky="nsew")
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(0, weight=1)

        container = card(shell)
        container.grid(row=0, column=0, sticky="n")
        container.columnconfigure(0, weight=1)

        header_frame = ttkb.Frame(container)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.columnconfigure(0, weight=1)

        self.header_label = section_title(header_frame, f"Subject: {self.subject}")
        self.header_label.grid(row=0, column=0, sticky="w")
        self.difficulty_label = ttkb.Label(
            header_frame, text=f"Difficulty: {self.current_difficulty}/5", style="Meta.TLabel"
        )
        self.difficulty_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.tip_label = ttkb.Label(container, text="", style="Meta.TLabel")
        self.tip_label.grid(row=1, column=0, sticky="w", pady=(SPACING_12, 0))
        self.difficulty_notice = ttkb.Label(container, text="", style="Meta.TLabel")
        self.difficulty_notice.grid(row=2, column=0, sticky="w", pady=(4, SPACING_12))

        self.question_label = ttkb.Label(
            container, text="", wraplength=760, justify="left", style="Subtitle.TLabel"
        )
        self.question_label.grid(row=3, column=0, sticky="w", pady=(0, SPACING_16))

        self.options_frame = ttkb.Frame(container)
        self.options_frame.grid(row=4, column=0, sticky="ew")
        self.options_frame.columnconfigure(0, weight=1)

        self.option_buttons: dict[str, ttkb.Button] = {}
        self.options_frame.configure(bootstyle="light")
        for key in ["A", "B", "C", "D"]:
            btn = ttkb.Button(
                self.options_frame,
                text="",
                command=lambda k=key: self.handle_answer(k),
                bootstyle="outline-primary",
                padding=(12, 8),
            )
            btn.grid(row=len(self.option_buttons), column=0, sticky="ew", pady=0)
            self.option_buttons[key] = btn

        self.feedback_label = ttkb.Label(container, text="", wraplength=760, justify="left", style="Meta.TLabel")
        self.feedback_label.grid(row=5, column=0, sticky="w", pady=(SPACING_12, SPACING_12))

        actions = ttkb.Frame(container)
        actions.grid(row=6, column=0, sticky="ew", pady=(SPACING_12, 0))
        actions.columnconfigure(0, weight=1, uniform="actions")
        actions.columnconfigure(1, weight=1, uniform="actions")
        actions.columnconfigure(2, weight=1, uniform="actions")

        self.tts_button = ttkb.Button(actions, text="Read question", command=self.speak_question, bootstyle="secondary")
        self.tts_button.grid(row=0, column=0, sticky="ew")
        self.next_button = primary_button(actions, "Next question", command=self.next_question)
        self.next_button.grid(row=0, column=1, sticky="ew")
        self.finish_button = secondary_button(actions, "Finish and home", command=self.end_quiz)
        self.finish_button.grid(row=0, column=2, sticky="ew")

    def on_show(self) -> None:
        user = getattr(self.controller, "current_user", None)
        if not user:
            messagebox.showerror("Error", "Please sign in first.")
            self.controller.show_frame("LoginView")
            return
        if self.session_id:
            quiz_service.end_session(self.session_id)
        self.session_id = quiz_service.start_session(user["user_id"])
        self.seen_question_ids.clear()
        self.correct_streak = 0
        self.session_attempts = 0
        self.session_correct = 0
        self.session_time_sum = 0
        self.session_tts_count = 0
        self.answer_locked = False
        self.current_difficulty = progress_service.get_last_attempt_difficulty(user["user_id"])
        self._update_difficulty_ui()
        self.tip_label.config(text=user_service.get_profile_tip(user.get("sen_profile")))
        self.load_question()

    def load_question(self) -> None:
        self.feedback_label.config(text="")
        self.feedback_label.grid_remove()
        self.used_tts_for_question = False
        self.difficulty_notice.config(text="")
        self.difficulty_notice.grid_remove()
        self.answer_locked = False
        self.next_button.config(state="normal")

        question, actual_difficulty = quiz_service.get_question_with_fallback(
            self.subject, self.current_difficulty, self.seen_question_ids
        )
        if not question:
            self.current_question = None
            self._disable_question_inputs()
            self.feedback_label.config(text="No more questions available.")
            self.next_button.config(state="disabled")
            return

        if actual_difficulty is not None and actual_difficulty != self.current_difficulty:
            self.current_difficulty = actual_difficulty
            self.difficulty_notice.config(text=f"Moved to difficulty {self.current_difficulty} due to availability.")
            self.difficulty_notice.grid()
            self._update_difficulty_ui()

        self.current_question = question
        self.seen_question_ids.add(question["question_id"])
        self.question_label.config(text=question["question_text"])

        options = {
            "A": question.get("option_a", ""),
            "B": question.get("option_b", ""),
            "C": question.get("option_c", ""),
            "D": question.get("option_d", ""),
        }
        for idx, (key, text) in enumerate(options.items()):
            btn = self.option_buttons[key]
            if text:
                btn.config(text=f"{key}. {text}", state="normal")
                btn.grid(row=idx, column=0, sticky="ew", pady=6)
            else:
                btn.grid_remove()

        self.question_start_time = time.monotonic()
        self._update_tts_visibility()

    def handle_answer(self, option_key: str) -> None:
        if self.answer_locked:
            return
        if not self.current_question:
            return
        self.answer_locked = True
        elapsed = int(time.monotonic() - self.question_start_time)
        correct_option = self.current_question.get("correct_option")
        is_correct = option_key == correct_option

        quiz_service.record_attempt(
            user_id=self.controller.current_user_id or self.controller.current_user.get("user_id"),
            session_id=self.session_id,
            question_id=self.current_question["question_id"],
            selected_option=option_key,
            is_correct=is_correct,
            time_spent_sec=elapsed,
            used_tts=self.used_tts_for_question,
        )

        self.session_attempts += 1
        self.session_time_sum += elapsed
        if self.used_tts_for_question:
            self.session_tts_count += 1
        if is_correct:
            self.session_correct += 1
            self.correct_streak += 1
        else:
            self.correct_streak = 0

        explanation = self.current_question.get("explanation") or ""
        result_text = self._format_feedback(is_correct, correct_option, explanation)
        self.feedback_label.config(text=result_text)
        self.feedback_label.grid()

        for btn in self.option_buttons.values():
            btn.config(state="disabled")

        previous = self.current_difficulty
        self.current_difficulty = int(next_difficulty(is_correct, self.current_difficulty))
        if self.current_difficulty != previous:
            direction = "increased" if self.current_difficulty > previous else "decreased"
            self.difficulty_notice.config(
                text=f"Difficulty {direction} to {self.current_difficulty}."
            )
        self._update_difficulty_ui()

        self._create_recommendation(is_correct, elapsed)

    def next_question(self) -> None:
        for btn in self.option_buttons.values():
            btn.config(state="normal")
        self.load_question()

    def end_quiz(self) -> None:
        if self.session_id:
            quiz_service.end_session(self.session_id)
            self.session_id = None
        self.controller.show_frame("DashboardView")

    def _update_tts_visibility(self) -> None:
        user = getattr(self.controller, "current_user", None)
        enabled = bool(user.get("tts_enabled")) if user else False
        if enabled:
            self.tts_button.grid()
        else:
            self.tts_button.grid_remove()

    def _update_difficulty_ui(self) -> None:
        self.difficulty_label.config(text=f"Difficulty: {self.current_difficulty}/5")

    def _disable_question_inputs(self) -> None:
        for btn in self.option_buttons.values():
            btn.config(state="disabled")

    def _format_feedback(self, is_correct: bool, correct_option: str, explanation: str) -> str:
        user = getattr(self.controller, "current_user", None) or {}
        profile = user.get("sen_profile")
        if profile == "autism":
            status = "Correct" if is_correct else "Incorrect"
            message = f"Result: {status}\nCorrect option: {correct_option}"
            if explanation:
                message += f"\nExplanation: {explanation}"
            return message

        message = "Correct!" if is_correct else f"Incorrect. Correct answer: {correct_option}"
        if explanation:
            message += f"\nExplanation: {explanation}"
        return message

    def _create_recommendation(self, is_correct: bool, elapsed: int) -> None:
        user = getattr(self.controller, "current_user", None) or {}
        user_id = user.get("user_id")
        if not user_id:
            return

        avg_time = self.session_time_sum / self.session_attempts if self.session_attempts else 0
        profile = user.get("sen_profile")
        tts_enabled = bool(user.get("tts_enabled"))

        rec_type = "general"
        message = "Keep going! Try another question."
        metadata = {"avg_time_sec": round(avg_time, 1), "elapsed_sec": elapsed}

        if not is_correct:
            rec_type = "review"
            message = "Try an easier difficulty next or review the concept."
        elif self.correct_streak >= 3:
            rec_type = "challenge"
            message = "Great streak! Consider trying a harder difficulty."
        elif avg_time > 15:
            rec_type = "support"
            message = "You are taking longer than usual. Consider enabling TTS or taking a short break."
        elif profile == "dyslexia" and not tts_enabled:
            rec_type = "accessibility"
            message = "Consider enabling TTS to support reading."

        try:
            recommendation_service.add_recommendation(
                user_id=user_id,
                session_id=self.session_id,
                rec_type=rec_type,
                message=message,
                metadata_json=metadata,
            )
        except Exception:
            # Recommendation failures should not block quiz flow.
            return

    def speak_question(self) -> None:
        if not self.current_question:
            return
        try:
            filepath = tts_service.speak(
                text=self.current_question.get("question_text", ""),
                cache_key=f"q_{self.current_question['question_id']}",
            )
        except ImportError:
            messagebox.showerror("Error", "gTTS is not installed. Please run: pip install -r requirements.txt")
            return
        except Exception as exc:
            messagebox.showerror("Error", f"Could not generate audio: {exc}")
            return

        try:
            tts_service.play(filepath)
        except ImportError as exc:
            messagebox.showerror("Error", f"Audio playback failed: {exc}")
            return
        except Exception as exc:
            messagebox.showerror("Error", f"Audio playback failed: {exc}")
            return

        self.used_tts_for_question = True
