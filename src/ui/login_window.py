"""Окно авторизации с капчей-пазлом."""
import tkinter as tk
from tkinter import messagebox
from src.auth import authenticate
from src.config import APP_NAME, MAX_FAILED_ATTEMPTS


class LoginWindow:
    """Окно входа в систему."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{APP_NAME} — Авторизация")
        self.root.geometry("400x370")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        self.captcha_passed = False
        self.captcha_fails = 0
        
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса."""
        main_frame = tk.Frame(self.root, bg="#ffffff", highlightbackground="#cccccc", highlightthickness=1)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=320)
        
        tk.Label(main_frame, text=APP_NAME, font=("Arial", 16, "bold"),
                 bg="#ffffff", fg="#2196F3").pack(pady=(15, 0))
        tk.Label(main_frame, text="Вход в систему", font=("Arial", 10),
                 bg="#ffffff", fg="#666666").pack(pady=(0, 15))
        
        # Логин
        tk.Label(main_frame, text="Логин:", font=("Arial", 10),
                 bg="#ffffff", fg="#333333").pack(anchor="w", padx=30)
        self.login_var = tk.StringVar()
        self.login_entry = tk.Entry(main_frame, textvariable=self.login_var, width=35,
                                     font=("Arial", 10), relief="solid", bd=1,
                                     state="disabled", disabledbackground="#f0f0f0")
        self.login_entry.pack(padx=30, pady=(2, 8))
        
        # Пароль
        tk.Label(main_frame, text="Пароль:", font=("Arial", 10),
                 bg="#ffffff", fg="#333333").pack(anchor="w", padx=30)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(main_frame, textvariable=self.password_var, width=35,
                                        font=("Arial", 10), relief="solid", bd=1, show="•",
                                        state="disabled", disabledbackground="#f0f0f0")
        self.password_entry.pack(padx=30, pady=(2, 10))
        
        # Капча
        captcha_frame = tk.Frame(main_frame, bg="#ffffff")
        captcha_frame.pack(pady=5)
        
        self.captcha_var = tk.BooleanVar(value=False)
        self.captcha_check = tk.Checkbutton(captcha_frame, text="Я не робот",
                                             variable=self.captcha_var,
                                             state="disabled", bg="#ffffff",
                                             font=("Arial", 10))
        self.captcha_check.pack(side="left")
        
        self.captcha_btn = tk.Button(captcha_frame, text="Пройти проверку",
                                      command=self.show_captcha,
                                      bg="#FF9800", fg="#ffffff", font=("Arial", 9),
                                      relief="flat", cursor="hand2", padx=10)
        self.captcha_btn.pack(side="left", padx=10)
        
        # Кнопка Войти
        self.login_button = tk.Button(main_frame, text="Войти", command=self.do_login,
                                       bg="#2196F3", fg="#ffffff", font=("Arial", 11, "bold"),
                                       relief="flat", cursor="hand2", width=20, height=1,
                                       state="disabled")
        self.login_button.pack(pady=(10, 5))
        
        self.root.bind("<Return>", lambda event: self.do_login())
    
    def show_captcha(self):
        """Открывает окно капчи."""
        self.root.withdraw()
        captcha_window = tk.Toplevel(self.root)
        captcha_solved = [False]
        attempts_exceeded = [False]
        
        from src.ui.captcha_window import CaptchaWindow
        
        def on_fail():
            self.captcha_fails += 1
            if self.captcha_fails >= MAX_FAILED_ATTEMPTS:
                attempts_exceeded[0] = True
        
        def on_success():
            captcha_solved[0] = True
        
        CaptchaWindow(captcha_window, self.root, on_fail, on_success)
        self.root.wait_window(captcha_window)
        
        if attempts_exceeded[0]:
            self.captcha_btn.config(text="Заблокировано", bg="#E53935", state="disabled")
            self.root.deiconify()
            messagebox.showerror("Доступ заблокирован", 
                                "Слишком много попыток. Попробуйте позже.")
            return
        
        if captcha_solved[0]:
            self.captcha_passed = True
            self.captcha_var.set(True)
            self.login_entry.config(state="normal")
            self.password_entry.config(state="normal")
            self.login_button.config(state="normal", bg="#4CAF50")
            self.captcha_btn.config(text="Пройдено ✓", bg="#4CAF50", state="disabled")
            self.login_entry.focus()
        else:
            self.captcha_var.set(False)
        
        self.root.deiconify()
    
    def do_login(self):
        """Обработчик входа."""
        if not self.captcha_passed:
            messagebox.showwarning("Проверка", "Сначала пройдите проверку «Я не робот».")
            return
        
        login = self.login_var.get().strip()
        password = self.password_var.get()
        
        if not login or not password:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")
            return
        
        user = authenticate(login, password)
        
        if user is None:
            messagebox.showerror("Ошибка авторизации",
                                "Вы ввели неверный логин или пароль.\nПожалуйста проверьте ещё раз введенные данные.")
        elif user.get('blocked'):
            messagebox.showerror("Доступ заблокирован", 
                                "Вы заблокированы. Обратитесь к администратору.")
        else:
            messagebox.showinfo("Успех", "Вы успешно авторизовались.")
            if user['password_must_change']:
                self.root.withdraw()
                change_window = tk.Toplevel(self.root)
                from src.ui.change_password_window import ChangePasswordWindow
                ChangePasswordWindow(change_window, user['user_id'], self.root)
            else:
                self.open_dashboard(user)
    
    def open_dashboard(self, user: dict):
        """Открывает интерфейс в зависимости от роли."""
        self.root.destroy()
        root = tk.Tk()
        if user['role'] == 'Администратор':
            from src.ui.admin_panel_window import AdminPanelWindow
            AdminPanelWindow(root, user)
        else:
            root.title(f"{APP_NAME} — {user['role']}")
            root.geometry("400x200")
            tk.Label(root, text=f"Добро пожаловать, {user['login']}!\nРоль: {user['role']}",
                     font=("Arial", 14)).pack(padx=50, pady=50)
        root.mainloop()