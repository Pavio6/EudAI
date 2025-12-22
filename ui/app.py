import tkinter as tk


def launch_app() -> None:
    """Start the Tkinter main window."""
    root = tk.Tk()
    root.title("EduAI")
    root.geometry("400x200")

    label = tk.Label(root, text="EduAI 启动成功", font=("Arial", 16))
    label.pack(expand=True)

    root.mainloop()
