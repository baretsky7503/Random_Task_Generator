import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
from datetime import datetime


class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator - Генератор случайных задач")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Файлы для хранения данных
        self.tasks_file = "tasks.json"
        self.history_file = "history.json"

        # Загрузка данных
        self.tasks = self.load_tasks()
        self.history = self.load_history()

        # Текущая сгенерированная задача
        self.current_task = None

        # Создание интерфейса
        self.create_task_frame()
        self.create_generate_frame()
        self.create_history_frame()
        self.create_filter_frame()
        self.create_add_task_frame()

        # Обновление отображения
        self.refresh_history_display()
        self.update_task_list_display()

    def load_tasks(self):
        """Загрузка списка задач из JSON"""
        default_tasks = [
            {"text": "Прочитать статью", "category": "учёба"},
            {"text": "Сделать зарядку", "category": "спорт"},
            {"text": "Написать отчёт", "category": "работа"},
            {"text": "Выучить 10 новых слов", "category": "учёба"},
            {"text": "Пробежка 2 км", "category": "спорт"},
            {"text": "Позвонить клиенту", "category": "работа"},
            {"text": "Посмотреть вебинар", "category": "учёба"},
            {"text": "Сделать план на день", "category": "работа"},
            {"text": "Отжаться 20 раз", "category": "спорт"},
            {"text": "Прочитать книгу 30 минут", "category": "учёба"},
            {"text": "Сходить в спортзал", "category": "спорт"},
            {"text": "Закончить проект", "category": "работа"}
        ]

        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Сохраняем задачи по умолчанию
            self.save_tasks(default_tasks)
            return default_tasks

    def save_tasks(self, tasks=None):
        """Сохранение списка задач в JSON"""
        if tasks is None:
            tasks = self.tasks
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)

    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self):
        """Сохранение истории в JSON"""
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    def create_task_frame(self):
        """Фрейм для отображения текущей задачи"""
        self.task_frame = tk.LabelFrame(self.root, text="Текущая задача", font=("Arial", 12, "bold"), padx=10, pady=10)
        self.task_frame.pack(fill="x", padx=10, pady=5)

        self.current_task_label = tk.Label(self.task_frame, text="Нажмите 'Сгенерировать задачу'",
                                           font=("Arial", 14, "italic"), fg="#7f8c8d")
        self.current_task_label.pack(pady=20)

    def create_generate_frame(self):
        """Фрейм с кнопкой генерации"""
        generate_frame = tk.Frame(self.root)
        generate_frame.pack(pady=10)

        self.generate_btn = tk.Button(generate_frame, text="🎲 Сгенерировать задачу",
                                      command=self.generate_task,
                                      bg="#2c3e50", fg="white", font=("Arial", 12, "bold"),
                                      width=25, height=2)
        self.generate_btn.pack()

    def create_history_frame(self):
        """Фрейм для отображения истории"""
        history_frame = tk.LabelFrame(self.root, text="История задач", font=("Arial", 12, "bold"), padx=10, pady=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создание таблицы для истории
        columns = ("Время", "Задача", "Категория")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)

        self.history_tree.heading("Время", text="Время")
        self.history_tree.heading("Задача", text="Задача")
        self.history_tree.heading("Категория", text="Категория")

        self.history_tree.column("Время", width=150)
        self.history_tree.column("Задача", width=350)
        self.history_tree.column("Категория", width=100)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления историей
        btn_frame = tk.Frame(history_frame)
        btn_frame.pack(fill="x", pady=5)

        self.clear_history_btn = tk.Button(btn_frame, text="🗑 Очистить историю",
                                           command=self.clear_history,
                                           bg="#e74c3c", fg="white", font=("Arial", 9))
        self.clear_history_btn.pack(side="left", padx=5)

    def create_filter_frame(self):
        """Фрейм для фильтрации истории"""
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация истории", font=("Arial", 12, "bold"), padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Фильтр по категории:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)

        self.filter_category = tk.StringVar(value="все")
        categories_frame = tk.Frame(filter_frame)
        categories_frame.grid(row=0, column=1, padx=5, pady=5)

        tk.Radiobutton(categories_frame, text="Все", variable=self.filter_category,
                       value="все", command=self.apply_filter).pack(side="left", padx=5)
        tk.Radiobutton(categories_frame, text="📚 Учёба", variable=self.filter_category,
                       value="учёба", command=self.apply_filter).pack(side="left", padx=5)
        tk.Radiobutton(categories_frame, text="🏃 Спорт", variable=self.filter_category,
                       value="спорт", command=self.apply_filter).pack(side="left", padx=5)
        tk.Radiobutton(categories_frame, text="💼 Работа", variable=self.filter_category,
                       value="работа", command=self.apply_filter).pack(side="left", padx=5)

        self.filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter,
                                    bg="#3498db", fg="white", font=("Arial", 9))
        self.filter_btn.grid(row=0, column=2, padx=10)

    def create_add_task_frame(self):
        """Фрейм для добавления новых задач"""
        add_frame = tk.LabelFrame(self.root, text="Добавить новую задачу", font=("Arial", 12, "bold"), padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(add_frame, text="Название задачи:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.new_task_entry = tk.Entry(add_frame, width=40, font=("Arial", 10))
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Категория:", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5)
        self.new_task_category = ttk.Combobox(add_frame, values=["учёба", "спорт", "работа"], width=10,
                                              state="readonly")
        self.new_task_category.set("учёба")
        self.new_task_category.grid(row=0, column=3, padx=5, pady=5)

        self.add_task_btn = tk.Button(add_frame, text="➕ Добавить задачу", command=self.add_new_task,
                                      bg="#27ae60", fg="white", font=("Arial", 10))
        self.add_task_btn.grid(row=0, column=4, padx=10)

    def generate_task(self):
        """Генерация случайной задачи"""
        if not self.tasks:
            messagebox.showerror("Ошибка", "Список задач пуст! Добавьте хотя бы одну задачу.")
            return

        # Выбор случайной задачи
        self.current_task = random.choice(self.tasks)

        # Отображение текущей задачи
        self.current_task_label.config(
            text=f"✨ {self.current_task['text']} ✨",
            font=("Arial", 14, "bold"),
            fg="#2c3e50"
        )

        # Добавление в историю
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task": self.current_task['text'],
            "category": self.current_task['category']
        }
        self.history.append(history_entry)
        self.save_history()

        # Обновление отображения
        self.apply_filter()

    def apply_filter(self):
        """Применение фильтра к истории"""
        category_filter = self.filter_category.get()

        if category_filter == "все":
            filtered_history = self.history
        else:
            filtered_history = [h for h in self.history if h['category'] == category_filter]

        self.display_history(filtered_history)

    def display_history(self, history_list):
        """Отображение истории в таблице"""
        # Очистка таблицы
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Отображение записей (от новых к старым)
        for entry in reversed(history_list):
            # Получение эмодзи для категории
            category_emoji = {
                "учёба": "📚",
                "спорт": "🏃",
                "работа": "💼"
            }.get(entry['category'], "")

            self.history_tree.insert("", "end", values=(
                entry['timestamp'],
                entry['task'],
                f"{category_emoji} {entry['category']}"
            ))

    def refresh_history_display(self):
        """Обновление отображения истории"""
        self.apply_filter()

    def update_task_list_display(self):
        """Обновление информации о количестве задач (опционально)"""
        # Можно добавить отображение количества задач в статус-баре
        pass

    def add_new_task(self):
        """Добавление новой задачи"""
        task_text = self.new_task_entry.get().strip()
        task_category = self.new_task_category.get()

        # Проверка на пустую строку
        if not task_text:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")
            return

        # Проверка на дубликат
        if any(task['text'].lower() == task_text.lower() for task in self.tasks):
            messagebox.showwarning("Предупреждение", "Такая задача уже существует!")
            return

        # Добавление задачи
        new_task = {"text": task_text, "category": task_category}
        self.tasks.append(new_task)
        self.save_tasks()

        # Очистка полей
        self.new_task_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", f"Задача \"{task_text}\" добавлена в список!")

    def clear_history(self):
        """Очистка истории"""
        if not self.history:
            messagebox.showinfo("Информация", "История уже пуста.")
            return

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.apply_filter()
            messagebox.showinfo("Успех", "История очищена!")


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()