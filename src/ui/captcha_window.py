"""Окно капчи — сборка пазла из 4 фрагментов."""
import tkinter as tk
from tkinter import messagebox
import os
import random


class CaptchaWindow:
    """Окно с пазлом-капчей."""
    
    def __init__(self, window: tk.Toplevel, login_window: tk.Tk, fail_callback, success_callback):
        self.window = window
        self.login_window = login_window
        self.fail_callback = fail_callback
        self.success_callback = success_callback
        self.pieces = []
        self.slots = {}
        self.piece_size = 117
        
        window.title("Проверка безопасности — соберите пазл")
        window.geometry("668x668")
        window.resizable(False, False)
        window.configure(bg="#f5f5f5")
        window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.pieces_dir = os.path.join(os.path.dirname(__file__), "captcha_pieces")
        self.selected_piece = None
        self.selected_label = None
        
        self.build_ui()
    
    def on_close(self):
        self.window.destroy()
        self.login_window.deiconify()
    
    def build_ui(self):
        # Очищаем старые виджеты
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.pieces = []
        self.slots = {}
        self.selected_piece = None
        self.selected_label = None
        
        tk.Label(self.window, text="Соберите изображение — кликните на фрагмент, затем на ячейку",
                 font=("Arial", 11, "bold"), bg="#f5f5f5").pack(pady=15)
        
        # Загружаем фрагменты
        self.piece_images = {}
        for i in range(1, 5):
            path = os.path.join(self.pieces_dir, f"{i}.png")
            img = tk.PhotoImage(file=path)
            img = img.subsample(6, 6)
            self.piece_images[i] = img
        
        # Сетка сборки 2x2
        main = tk.Frame(self.window, bg="#f5f5f5")
        main.pack(expand=True)
        
        grid_frame = tk.Frame(main, bg="#666666", bd=1)
        grid_frame.pack()
        
        for row in range(2):
            for col in range(2):
                cell = tk.Frame(grid_frame, width=self.piece_size, height=self.piece_size,
                               bg="#ffffff", relief="sunken", bd=1)
                cell.grid(row=row, column=col, padx=1, pady=1)
                cell.pack_propagate(False)
                cell.grid_propagate(False)
                
                lbl = tk.Label(cell, text="?", font=("Arial", 16, "bold"),
                              bg="#ffffff", fg="#cccccc")
                lbl.place(relx=0.5, rely=0.5, anchor="center")
                
                cell.bind("<Button-1>", lambda e, r=row, c=col: self.place_piece(r, c))
                lbl.bind("<Button-1>", lambda e, r=row, c=col: self.place_piece(r, c))
                
                self.slots[(row, col)] = {"label": lbl, "piece": None}
        
        # Разделитель
        tk.Frame(self.window, bg="#cccccc", height=1).pack(fill="x", padx=50, pady=15)
        
        # Фрагменты
        tk.Label(self.window, text="Фрагменты:", font=("Arial", 10, "bold"),
                 bg="#f5f5f5").pack()
        
        pieces_frame = tk.Frame(self.window, bg="#f5f5f5")
        pieces_frame.pack(pady=10)
        
        piece_order = [1, 2, 3, 4]
        random.shuffle(piece_order)
        
        for num in piece_order:
            lbl = tk.Label(pieces_frame, image=self.piece_images[num],
                          bg="#ffffff", relief="raised", bd=2, cursor="hand2")
            lbl.image = self.piece_images[num]
            lbl.pack(side="left", padx=8)
            lbl.bind("<Button-1>", lambda e, n=num, l=lbl: self.select_piece(n, l))
            self.pieces.append({"num": num, "label": lbl, "placed": False})
    
    def select_piece(self, piece_num, label):
        for p in self.pieces:
            if p["num"] == piece_num and p["placed"]:
                return
        self.selected_piece = piece_num
        if self.selected_label:
            self.selected_label.config(relief="raised", bd=2, bg="#ffffff")
        self.selected_label = label
        label.config(relief="sunken", bd=4, bg="#E3F2FD")
    
    def place_piece(self, row, col):
        if self.selected_piece is None:
            return
        
        slot_data = self.slots[(row, col)]
        old = slot_data["piece"]
        if old is not None:
            for p in self.pieces:
                if p["num"] == old:
                    p["placed"] = False
                    p["label"].config(relief="raised", bd=2, bg="#ffffff")
        
        img = self.piece_images[self.selected_piece]
        slot_data["label"].config(image=img, text="")
        slot_data["label"].image = img
        slot_data["piece"] = self.selected_piece
        
        for p in self.pieces:
            if p["num"] == self.selected_piece:
                p["placed"] = True
                p["label"].config(relief="flat", bg="#C8E6C9")
        
        self.selected_piece = None
        if self.selected_label:
            self.selected_label.config(relief="raised", bd=2, bg="#ffffff")
        self.selected_label = None
        
        # Автопроверка
        if all(self.slots[pos]["piece"] is not None for pos in self.slots):
            self.window.after(300, self.check_puzzle)
    
    def check_puzzle(self):
        correct = {(0, 0): 1, (0, 1): 2, (1, 0): 3, (1, 1): 4}
        
        if all(self.slots[pos]["piece"] == num for pos, num in correct.items()):
            messagebox.showinfo("Успех", "Пазл собран верно!\nПроверка пройдена.")
            self.success_callback()
            self.window.destroy()
        else:
            messagebox.showerror("Ошибка", "Пазл собран неверно.\nПопробуйте ещё раз.")
            self.fail_callback()
            self.window.destroy()