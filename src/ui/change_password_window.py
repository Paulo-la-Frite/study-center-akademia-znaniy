"""Окно смены пароля при первом входе."""
import tkinter as tk
from tkinter import ttk, messagebox
from src.auth import change_password
from src.config import APP_NAME


class ChangePasswordWindow:
    """Окно принудительной смены пароля."""
    
    def __init__(self, window: tk.Toplevel, user_id: int, login_window: tk.Tk):
        self.window = window
        self.user_id = user_id
        self.login_window = login_window
        
        window.title(f"{APP_NAME} — Смена пароля")
        window.geometry("420x320")
        window.resizable(False, False)
        window.configure(bg="#f5f5f5")
        
        # Запрещаем закрыть окно
        window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Центрирование
        window.update_idletasks()
        w = window.winfo_width()
        h = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (w // 2)
        y = (window.winfo_screenheight() // 2) - (h // 2)
        window.geometry(f"{w}x{h}+{x}+{y}")
        
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса."""
        main_frame = tk.Frame(self.window, bg="#ffffff", highlightbackground="#cccccc", highlightthickness=1)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=360, height=260)
        
        tk.Label(main_frame, text="Требуется смена пароля", font=("Arial", 12, "bold"),
                 bg="#ffffff", fg="#E53935").pack(pady=(15, 3))
        tk.Label(main_frame, text="При первом входе необходимо\nустановить новый пароль.",
                 font=("Arial", 9), bg="#ffffff", fg="#666666").pack(pady=(0, 12))
        
        # Текущий пароль
        tk.Label(main_frame, text="Текущий пароль:", font=("Arial", 10),
                 bg="#ffffff").pack(anchor="w", padx=30)
        self.old_pass = tk.Entry(main_frame, show="•", width=35, font=("Arial", 10),
                                  relief="solid", bd=1)
        self.old_pass.pack(padx=30, pady=(2, 8))
        self.old_pass.focus()
        
        # Новый пароль
        tk.Label(main_frame, text="Новый пароль (мин. 6 символов):", font=("Arial", 10),
                 bg="#ffffff").pack(anchor="w", padx=30)
        self.new_pass = tk.Entry(main_frame, show="•", width=35, font=("Arial", 10),
                                  relief="solid", bd=1)
        self.new_pass.pack(padx=30, pady=(2, 8))
        
        # Подтверждение
        tk.Label(main_frame, text="Подтвердите новый пароль:", font=("Arial", 10),
                 bg="#ffffff").pack(anchor="w", padx=30)
        self.confirm_pass = tk.Entry(main_frame, show="•", width=35, font=("Arial", 10),
                                      relief="solid", bd=1)
        self.confirm_pass.pack(padx=30, pady=(2, 12))
        
        # Кнопка
        self.change_btn = tk.Button(main_frame, text="Изменить пароль", command=self.do_change,
                                     bg="#4CAF50", fg="#ffffff", font=("Arial", 11, "bold"),
                                     relief="flat", cursor="hand2", width=20)
        self.change_btn.pack()
        
        self.window.bind("<Return>", lambda e: self.do_change())
    
    def do_change(self):
        """Обработчик смены пароля."""
        old = self.old_pass.get()
        new = self.new_pass.get()
        confirm = self.confirm_pass.get()
        
        if not old or not new or not confirm:
            messagebox.showwarning("Предупреждение", "Все поля обязательны для заполнения.")
            return
        
        if new != confirm:
            messagebox.showerror("Ошибка", "Новый пароль и подтверждение не совпадают.")
            return
        
        success, message = change_password(self.user_id, old, new)
        
        if success:
            messagebox.showinfo("Успех", message)
            self.window.destroy()
            self.login_window.deiconify()
        else:
            messagebox.showerror("Ошибка", message)