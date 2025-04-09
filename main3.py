import tkinter as tk
from operator import index
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math
import numpy as np

# Глобальная переменная для хранения объекта Canvas
plot_canvas = None

# Функция для отображения графика
def plot_data(mas_y, mas_p, mas_n, F_theoretical, F_empirical):
    global plot_canvas

    # Очистка предыдущего графика, если он существует
    if plot_canvas:
        plot_canvas.get_tk_widget().destroy()

    # Создание нового графика
    fig = Figure(figsize=(7, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    mas_y1 = [0] + mas_y
    mas_p1 = [0] + mas_p
    mas_n1 = [0] + mas_n

    if len(mas_y) == 1:
        ax1.scatter(mas_y1, mas_p1, label="Теоретическая вероятность", color='blue')
        ax1.scatter(mas_y1, mas_n1, label="Выборочная вероятность", color='red')
        ax1.set_title("Распределение вероятностей")
        ax1.set_xlabel("Значение")
        ax1.set_ylabel("Вероятность")
        ax1.legend()
    else:
        # График распределения вероятностей
        ax1.plot(mas_y, mas_p, label="Теоретическая вероятность", color='blue')
        ax1.plot(mas_y, mas_n, label="Выборочная вероятность", color='red', linestyle='--')
        ax1.set_title("Распределение вероятностей")
        ax1.set_xlabel("Значение")
        ax1.set_ylabel("Вероятность")
        ax1.legend()

    mas_y1 = [0] + mas_y
    F_theoretical1 = np.array(F_theoretical)
    F_theoretical1 = F_theoretical1.tolist()
    F_theoretical1.insert(0, 0.3)

    if len(F_theoretical) == 1:
        ax2.scatter(mas_y1, F_theoretical1, label="Теоретическая F(x)", color='blue')
        ax2.scatter(mas_y, F_empirical, label="Выборочная F_hat(x)", color='red')
        ax2.set_title("Функция распределения")
        ax2.set_xlabel("Значение")
        ax2.set_ylabel("F(x)")
        ax2.legend()
    else:
        # График функции распределения
        ax2.step(mas_y1, F_theoretical1, label="Теоретическая F(x)", color='blue')
        ax2.step(mas_y, F_empirical, label="Выборочная F_hat(x)", color='red', linestyle='--')
        ax2.set_title("Функция распределения")
        ax2.set_xlabel("Значение")
        ax2.set_ylabel("F(x)")
        ax2.legend()

    # Отображение графика в Tkinter
    plot_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    plot_canvas.draw()
    plot_canvas.get_tk_widget().pack()

# Функция для вычисления выборки и построения графика
def run_experiment():
    try:
        p = float(entry_p.get())  # Вероятность наблюдения
        n = int(entry_n.get())    # Количество испытаний

        if not (0 < p <= 1):
            raise ValueError("p должно быть в пределах (0, 1].")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные значения вероятности p (0 < p ≤ 1) и числа испытаний.")
        return

    # Генерация выборки
    mas_y = []  # Список для значений наблюдения
    for _ in range(n):
        cycles = 0
        while True:
            cycles += 1
            if random.random() < p:
                break
        mas_y.append(cycles)

    max_cycle = max(mas_y)  # Максимальное количество циклов для наблюдения
    mas_unique = list(range(1, max_cycle + 1))  # Уникальные значения циклов

    # Шансы и вероятности
    mas_ni = [mas_y.count(i) for i in mas_unique]  # Шансы появления цикла
    mas_n = [ni / n for ni in mas_ni]  # Выборочные вероятности (относительные частоты)
    # mas_p = [0]
    mas_p = [(1 - p) ** (i - 1) * p for i in mas_unique]  # Теоретические вероятности

    mas_pair = []

    c = 0
    mas_y = sorted(mas_y)
    for i in range(len(mas_ni)):
        if mas_ni[i] > 0:
            c += 1
            mas_pair.append(i)
    if c == 1:
        Me = mas_unique[max_cycle - 1]
    else:
        if len(mas_y) % 2 == 1:
            Me = mas_y[(len(mas_y) - 1) // 2]  # Медиана
        else:
            Me = ((mas_y[(len(mas_y) - 1) // 2] + mas_y[((len(mas_y) - 1) // 2) + 1]) / 2)

    # Теоретическая и выборочная функция распределения
    F_theoretical = np.cumsum(mas_p)
    F_empirical = np.cumsum(mas_n)

    # Полученные статистические характеристики
    En = sum(i * mas_p[i - 1] for i in mas_unique)  # Теоретическое математическое ожидание
    Dn = sum((i ** 2) * mas_p[i - 1] for i in mas_unique) - En ** 2  # Теоретическая дисперсия

    x_cherta = sum(i * mas_n[i - 1] for i in mas_unique)  # Выборочное среднее
    S2 = sum(((i - x_cherta) ** 2) * mas_n[i - 1] for i in mas_unique)  # Выборочная дисперсия

    R = len(mas_pair)  # Разброс

    max_diff = 0
    for i in range(len(F_theoretical)):
        if abs(F_theoretical[i] - F_empirical[i]) > max_diff:
            max_diff = abs(F_theoretical[i] - F_empirical[i])

    # Максимальное отклонение вероятностей и выборочной функции распределения
    max_deviation = max(abs(mas_n[i] - mas_p[i]) for i in range(len(mas_p)))

    # Вывод результатов
    result_text.set(f"E₀ = {En:.4f}\nD₀ = {Dn:.4f}\n\nМₓ = {x_cherta:.4f}\nS² = {S2:.4f}\n|E₀ - Мₓ| = {abs(En - x_cherta):.4f}\n|D₀ - S²| = {abs(Dn - S2):.4f}\nMe = {Me}\nR = {R}\nMax |n_j/n - P(О = y_j)| = {max_deviation:.4f}\n|max_D| = {max_diff}")

    table_frame = tk.Frame(root)
    table_frame.grid(row=4, column=0, columnspan=2, pady=10)

    table = ttk.Treeview(table_frame, columns=("y_j", "P_theor", "n_j/n", "Deviation"), show="headings", height=10)
    table.heading("y_j", text="Значение")
    table.heading("P_theor", text="P(О = y_j)")
    table.heading("n_j/n", text="n_j / n")
    table.heading("Deviation", text="|n_j/n - P(О = y_j)|")

    # Заполнение таблицы данных
    for i in range(len(mas_unique)):
        table.insert("", "end", values=(
            mas_unique[i],
            f"{mas_p[i]:.4f}",
            f"{mas_n[i]:.4f}",
            f"{abs(mas_n[i] - mas_p[i]):.4f}"
        ))

    table.pack()

    # Отображение графика
    plot_data(mas_unique, mas_p, mas_n, F_theoretical, F_empirical)

# Запуск приложения Tkinter
root = tk.Tk()
root.title("Лабораторная работа")

# Ввод значения вероятности p:
tk.Label(root, text="Вероятность наблюдения p:").grid(row=0, column=0)
entry_p = tk.Entry(root)
entry_p.grid(row=0, column=1)

tk.Label(root, text="Количество испытаний n:").grid(row=1, column=0)
entry_n = tk.Entry(root)
entry_n.grid(row=1, column=1)

# Кнопка запуска испытания
btn_run = tk.Button(root, text="Запустить испытание", command=run_experiment)
btn_run.grid(row=2, column=0, columnspan=2)

# Вывод результата
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify=tk.LEFT)
result_label.grid(row=3, column=0, columnspan=2)

# Поле для графика
plot_frame = tk.Frame(root)
plot_frame.grid(row=0, column=2, rowspan=5, padx=10, pady=10)

root.mainloop()
