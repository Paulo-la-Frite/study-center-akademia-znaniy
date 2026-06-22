"""Панель администратора."""
import tkinter as tk
from tkinter import ttk, messagebox
from src.auth import get_all_users, create_user
from src.config import APP_NAME
import src.db as db_module


class AdminPanelWindow:
    """Главное окно администратора."""
    
    def __init__(self, root: tk.Tk, user: dict):
        self.root = root
        self.user = user
        
        root.title(f"{APP_NAME} — Панель администратора")
        root.geometry("750x500")
        root.minsize(600, 400)
        root.configure(bg="#f5f5f5")
        
        self.build_ui()
    
    def build_ui(self):
        """Построение интерфейса."""
        # Шапка
        header = tk.Frame(self.root, bg="#2196F3", height=45)
        header.pack(fill="x")
        tk.Label(header, text=f"  {APP_NAME} — Панель администратора",
                 font=("Arial", 13, "bold"), bg="#2196F3", fg="#ffffff").pack(side="left", padx=15, pady=10)
        tk.Label(header, text=f"Администратор: {self.user['login']}  ",
                 font=("Arial", 10), bg="#2196F3", fg="#E3F2FD").pack(side="right", padx=15, pady=10)
        
        # Основная область
        content = tk.Frame(self.root, bg="#f5f5f5")
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Заголовок секции
        tk.Label(content, text="Управление пользователями", font=("Arial", 12, "bold"),
                 bg="#f5f5f5", fg="#333333").pack(anchor="w")
        
        # Кнопки
        btn_frame = tk.Frame(content, bg="#f5f5f5")
        btn_frame.pack(fill="x", pady=(10, 5))
        
        tk.Button(btn_frame, text="+ Добавить пользователя", command=self.show_add_user_dialog,
                  bg="#4CAF50", fg="#ffffff", font=("Arial", 10, "bold"),
                  relief="flat", cursor="hand2", padx=15, pady=4).pack(side="left")
        
        tk.Button(btn_frame, text="Обновить", command=self.refresh_users,
                  bg="#607D8B", fg="#ffffff", font=("Arial", 10),
                  relief="flat", cursor="hand2", padx=15, pady=4).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Снять блокировку", command=self.unblock_user,
                  bg="#FF9800", fg="#ffffff", font=("Arial", 10),
                  relief="flat", cursor="hand2", padx=15, pady=4).pack(side="left")
        
        # Таблица пользователей
        table_frame = tk.Frame(content, bg="#ffffff", highlightbackground="#cccccc", highlightthickness=1)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("user_id", "login", "role", "is_blocked", "attempts", "last_login")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("user_id", text="ID")
        self.tree.heading("login", text="Логин")
        self.tree.heading("role", text="Роль")
        self.tree.heading("is_blocked", text="Заблокирован")
        self.tree.heading("attempts", text="Попыток")
        self.tree.heading("last_login", text="Последний вход")
        
        self.tree.column("user_id", width=40, anchor="center")
        self.tree.column("login", width=150)
        self.tree.column("role", width=130)
        self.tree.column("is_blocked", width=100, anchor="center")
        self.tree.column("attempts", width=80, anchor="center")
        self.tree.column("last_login", width=150)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.refresh_users()
    
    def refresh_users(self):
        """Обновление списка пользователей."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        users = get_all_users()
        for u in users:
            last_login = u['last_login'].strftime("%d.%m.%Y %H:%M") if u['last_login'] else "Нет"
            self.tree.insert("", "end", values=(
                u['user_id'],
                u['login'],
                u['role'],
                "Да" if u['is_blocked'] else "Нет",
                u['failed_login_attempts'],
                last_login
            ))
    
    def show_add_user_dialog(self):
        """Диалог добавления пользователя."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("400x320")
        dialog.resizable(False, False)
        dialog.configure(bg="#f5f5f5")
        
        dialog.update_idletasks()
        w = dialog.winfo_width()
        h = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (dialog.winfo_screenheight() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        
        frame = tk.Frame(dialog, bg="#ffffff", highlightbackground="#cccccc", highlightthickness=1)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=270)
        
        tk.Label(frame, text="Новый пользователь", font=("Arial", 13, "bold"),
                 bg="#ffffff").pack(pady=(20, 15))
        
        tk.Label(frame, text="Логин:", bg="#ffffff", font=("Arial", 10)).pack(anchor="w", padx=30)
        login_entry = tk.Entry(frame, width=30, font=("Arial", 11), relief="solid", bd=1)
        login_entry.pack(padx=30, pady=(3, 12), ipady=3)
        login_entry.focus()
        
        tk.Label(frame, text="Пароль:", bg="#ffffff", font=("Arial", 10)).pack(anchor="w", padx=30)
        pass_entry = tk.Entry(frame, show="•", width=30, font=("Arial", 11), relief="solid", bd=1)
        pass_entry.pack(padx=30, pady=(3, 12), ipady=3)
        
        tk.Label(frame, text="Роль:", bg="#ffffff", font=("Arial", 10)).pack(anchor="w", padx=30)
        role_combo = ttk.Combobox(frame, values=['Студент', 'Преподаватель', 'Методист', 'Администратор'],
                                   state="readonly", width=27, font=("Arial", 11))
        role_combo.current(0)
        role_combo.pack(padx=30, pady=(3, 18), ipady=2)
        
        def add():
            login = login_entry.get().strip()
            password = pass_entry.get()
            role = role_combo.get()
            
            if not login or not password:
                messagebox.showwarning("Предупреждение", "Логин и пароль обязательны.")
                return
            
            success, message = create_user(login, password, role)
            if success:
                messagebox.showinfo("Успех", message)
                dialog.destroy()
                self.refresh_users()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(frame, text="Добавить", command=add,
                  bg="#4CAF50", fg="#ffffff", font=("Arial", 11, "bold"),
                  relief="flat", cursor="hand2", width=15, height=1).pack()
        
        dialog.bind("<Return>", lambda e: add())
    
    def unblock_user(self):
        """Снятие блокировки."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Информация", "Выберите пользователя в таблице.")
            return
        
        user_id = self.tree.item(selection[0])['values'][0]
        db_module.execute_query(
            "UPDATE users SET is_blocked = FALSE, failed_login_attempts = 0 WHERE user_id = %s",
            (user_id,)
        )
        messagebox.showinfo("Успех", "Блокировка снята.")
        self.refresh_users()