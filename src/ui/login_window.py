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
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        self.captcha_fails = 0
        self.current_login = ""
        self.current_password = ""
        
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса."""
        main_frame = tk.Frame(self.root, bg="#ffffff", highlightbackground="#cccccc", highlightthickness=1)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=260)
        
        tk.Label(main_frame, text=APP_NAME, font=("Arial", 16, "bold"),
                 bg="#ffffff", fg="#2196F3").pack(pady=(15, 0))
        tk.Label(main_frame, text="Вход в систему", font=("Arial", 10),
                 bg="#ffffff", fg="#666666").pack(pady=(0, 15))
        
        tk.Label(main_frame, text="Логин:", font=("Arial", 10),
                 bg="#ffffff", fg="#333333").pack(anchor="w", padx=30)
        self.login_var = tk.StringVar()
        self.login_entry = tk.Entry(main_frame, textvariable=self.login_var, width=35,
                                     font=("Arial", 10), relief="solid", bd=1)
        self.login_entry.pack(padx=30, pady=(2, 8))
        self.login_entry.focus()
        
        tk.Label(main_frame, text="Пароль:", font=("Arial", 10),
                 bg="#ffffff", fg="#333333").pack(anchor="w", padx=30)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(main_frame, textvariable=self.password_var, width=35,
                                        font=("Arial", 10), relief="solid", bd=1, show="•")
        self.password_entry.pack(padx=30, pady=(2, 15))
        
        self.login_button = tk.Button(main_frame, text="Войти", command=self.do_login,
                                       bg="#2196F3", fg="#ffffff", font=("Arial", 11, "bold"),
                                       relief="flat", cursor="hand2", width=20, height=1)
        self.login_button.pack(pady=(0, 5))
        
        self.root.bind("<Return>", lambda event: self.do_login())
        self.login_entry.bind("<Tab>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Tab>", lambda e: self.login_button.focus())
    
    def do_login(self):
        """Обработчик входа."""
        login = self.login_var.get().strip()
        password = self.password_var.get()
        
        if not login or not password:
            messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.\nЛогин и пароль обязательны.")
            return
        
        self.current_login = login
        self.current_password = password
        self.captcha_fails = 0
        
        # Проверяем, не заблокирован ли уже пользователь
        user_check = authenticate(login, password)
        if user_check and user_check.get('blocked'):
            messagebox.showerror("Доступ заблокирован", "Вы заблокированы. Обратитесь к администратору.")
            return
        
        # Показываем капчу
        self.show_captcha()
    
    def show_captcha(self):
        """Открывает окно капчи."""
        
        self.root.withdraw()
        captcha_window = tk.Toplevel(self.root)
        captcha_solved = [False]  # список для передачи по ссылке
        
        from src.ui.captcha_window import CaptchaWindow
        
        def on_fail():
            self.captcha_fails += 1
        
        def on_success():
            captcha_solved[0] = True
        
        CaptchaWindow(captcha_window, self.root, on_fail, on_success)
        self.root.wait_window(captcha_window)
        
        if captcha_solved[0]:
            self._do_authenticate()
        else:
            if self.captcha_fails >= MAX_FAILED_ATTEMPTS:
                self._block_and_return()
            else:
                self.root.deiconify()
    
    def _do_authenticate(self):
        """Выполняет аутентификацию после успешной капчи."""
        user = authenticate(self.current_login, self.current_password)
        
        if user is None:
            messagebox.showerror(
                "Ошибка авторизации",
                "Вы ввели неверный логин или пароль.\nПожалуйста проверьте ещё раз введенные данные."
            )
            self.root.deiconify()
        elif user.get('blocked'):
            messagebox.showerror(
                "Доступ заблокирован",
                "Вы заблокированы. Обратитесь к администратору."
            )
            self.root.deiconify()
        else:
            messagebox.showinfo("Успех", "Вы успешно авторизовались.")
            if user['password_must_change']:
                self.root.withdraw()
                change_window = tk.Toplevel(self.root)
                from src.ui.change_password_window import ChangePasswordWindow
                ChangePasswordWindow(change_window, user['user_id'], self.root)
            else:
                self.open_dashboard(user)
    
    def _block_and_return(self):
        """Блокирует попытки и возвращает на экран входа."""
        messagebox.showerror(
            "Доступ заблокирован",
            "Вы заблокированы. Обратитесь к администратору."
        )
        self.root.deiconify()
    
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