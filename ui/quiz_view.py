import time
import tkinter as tk
from tkinter import messagebox

from services import quiz_service, tts_service


class QuizView(tk.Frame):
    def __init__(self, parent: tk.Misc, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.subject = "Math"
        self.difficulty = 1
        self.seen_question_ids: set[int] = set()
        self.current_question: dict | None = None
        self.session_id: int | None = None
        self.question_start_time: float = 0.0
        self.used_tts_for_question = False
        self._build_widgets()

    def _build_widgets(self) -> None:
        header = tk.Label(self, text=f"Subject: {self.subject}", font=("Arial", 16))
        header.pack(pady=(20, 10))

        self.question_label = tk.Label(self, text="", wraplength=700, justify="left", font=("Arial", 14))
        self.question_label.pack(pady=10, padx=20, anchor="w")

        self.options_frame = tk.Frame(self)
        self.options_frame.pack(pady=10)

        self.option_buttons: dict[str, tk.Button] = {}
        for key in ["A", "B", "C", "D"]:
            btn = tk.Button(
                self.options_frame,
                text="",
                width=40,
                anchor="w",
                command=lambda k=key: self.handle_answer(k),
            )
            btn.pack(fill="x", pady=4)
            self.option_buttons[key] = btn

        self.feedback_label = tk.Label(self, text="", wraplength=700, justify="left", fg="blue")
        self.feedback_label.pack(pady=10, padx=20, anchor="w")

        actions = tk.Frame(self)
        actions.pack(pady=10)
        self.tts_button = tk.Button(actions, text="Read question", command=self.speak_question)
        self.tts_button.grid(row=0, column=0, padx=8)
        tk.Button(actions, text="Next question", command=self.next_question).grid(row=0, column=1, padx=8)
        tk.Button(actions, text="Finish and home", command=self.end_quiz).grid(row=0, column=2, padx=8)

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
        self.load_question()

    def load_question(self) -> None:
        self.feedback_label.config(text="")
        self.used_tts_for_question = False
        question = quiz_service.get_random_question(
            self.subject, self.difficulty, self.seen_question_ids
        )
        if not question:
            messagebox.showinfo("Info", "No more questions. Returning to dashboard.")
            self.end_quiz()
            return
        self.current_question = question
        self.seen_question_ids.add(question["question_id"])
        self.question_label.config(text=question["question_text"])

        options = {
            "A": question.get("option_a", ""),
            "B": question.get("option_b", ""),
            "C": question.get("option_c", ""),
            "D": question.get("option_d", ""),
        }
        for key, text in options.items():
            btn = self.option_buttons[key]
            if text:
                btn.config(text=f"{key}. {text}", state="normal")
                btn.pack(fill="x", pady=4)
            else:
                btn.pack_forget()

        self.question_start_time = time.monotonic()
        self._update_tts_visibility()

    def handle_answer(self, option_key: str) -> None:
        if not self.current_question:
            return
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

        explanation = self.current_question.get("explanation") or ""
        result_text = "Correct!" if is_correct else f"Incorrect. Correct answer: {correct_option}"
        if explanation:
            result_text += f"\nExplanation: {explanation}"
        self.feedback_label.config(text=result_text)

        for btn in self.option_buttons.values():
            btn.config(state="disabled")

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
