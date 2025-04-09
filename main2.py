import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import geom, kstest

# Параметры
p = float(input("Введите вероятность обнаружения: "))
if not 0 < p <= 1:
    raise ValueError("Вероятность должна быть в интервале (0, 1)")
N = int(input("Введите количество наблюдений: "))
if N <= 0:
    raise ValueError("Количество наблюдений должно быть больше 0")

# Моделирование
"""
Случайная величина, распределенная по геометрическому закону:
P(η=k)=(1−p)^(k-1)*p 
"""
eta = [geom.rvs(p) for _ in range(N)]

# Выборочные характеристики
"""
x: Среднее выборки.
S^2: Дисперсия выборки, вычисленная вручную.
Me: Медиана выборки, вычисленная вручную.
Размах выборки: Rb = max(η) − min(η).
"""
# Среднее
x = sum(eta) / len(eta)

# Выборочная дисперсия (S^2)
S2 = sum((xi - x) ** 2 for xi in eta) / len(eta)

# Медиана (Me)
sorted_eta = sorted(eta)
n = len(sorted_eta)
if n % 2 == 1:  # Нечётное количество элементов
    Me = sorted_eta[n // 2]
else:  # Чётное количество элементов
    Me = (sorted_eta[n // 2 - 1] + sorted_eta[n // 2]) / 2

# Размах
Rb = max(eta) - min(eta)

# Теоретические характеристики
E_eta = 1 / p
D_eta = (1 - p) / (p**2)

# Таблица
print("Таблица числовых характеристик:")
print("| Eη      | x       | |Eη - x| | Dη      | S²      | |Dη - S²| | Me      | Rb      |")
print("|---------|---------|---------|---------|---------|---------|---------|---------|---------|")
print(f"| {E_eta:.4f} | {x:.4f}   | {abs(E_eta - x):.4f} | {D_eta:.4f} | {S2:.4f}   | {abs(D_eta - S2):.4f} | {Me:.4f}   | {Rb:.4f}   |")

# Таблица проверки
unique_values, counts = np.unique(eta, return_counts=True)
probabilities = [(1-p)**(k-1)*p for k in unique_values]
table_data = {
    "yj": unique_values,
    "P({η = yj})": probabilities,
    "nj/n": counts / N,
    "|nj/n - P({η = yj})|": abs(counts / N - probabilities)
}

print("\nТаблица проверки:")
print("{:<10} {:<15} {:<15} {:<20}".format("yj", "P({η = yj})", "nj/n", "|nj/n - P({η = yj})|"))
for i in range(len(unique_values)):
    print("{:<10} {:<15.4f} {:<15.4f} {:<20.4f}".format(
        table_data["yj"][i],
        table_data["P({η = yj})"][i],
        table_data["nj/n"][i],
        table_data["|nj/n - P({η = yj})|"][i]
    ))
print(f"Максимальное отклонение: {np.max(table_data['|nj/n - P({η = yj})|']):.4f}")

# Графики функций распределения
if N == 1 or len(np.unique(eta)) == 1:
    max_eta = 2  # Минимальное значение для оси x, если все значения равны 1
else:
    max_eta = np.max(eta)

x_values = np.arange(1, np.max(eta) + 1)
theoretical_cdf = 1 - (1 - p)**(x_values - 1)
hist, bin_edges = np.histogram(eta, bins=np.arange(1, np.max(eta) + 2), density=True)
empirical_cdf = np.cumsum(hist)

plt.figure(figsize=(10, 6))
plt.step(x_values, theoretical_cdf, label='Теоретическая функция распределения')
plt.step(x_values, np.cumsum(hist), where='post', label='Выборочная функция распределения')
plt.xlabel('x')
plt.ylabel('F(x)')
plt.title('Теоретическая и выборочная функции распределения')
plt.legend()
plt.grid(True)
plt.show()
