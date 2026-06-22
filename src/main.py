"""Точка входа в приложение."""
import tkinter as tk
from src.ui.login_window import LoginWindow


def main():
    """Запуск приложения."""
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()