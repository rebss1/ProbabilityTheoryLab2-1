import random
import matplotlib.pyplot as plt
import numpy as np


def simulate_detection(p, num_trials):
    """
 Моделирует количество циклов наблюдения до обнаружения объекта.

 Аргументы:
 p: Вероятность обнаружения объекта за один цикл.
 num_trials: Количество попыток моделирования.

 Возвращается:
 Числовой массив, содержащий количество циклов до обнаружения для каждого испытания.
 """
    results = []
    for _ in range(num_trials):
        cycles = 0
        while random.random() > p:
            cycles += 1
        results.append(cycles)
    return np.array(results)


def calculate_characteristics(p, data):
    n = len(data)
    E_eta = 1 / p
    D_eta = (1 - p) / (p ** 2)
    x = np.mean(data)
    S_squared = np.var(data, ddof=1)
    med = np.median(data)
    Rb = np.max(data)

    return E_eta, D_eta, x, S_squared, med, Rb


def calculate_probabilities(data, p):
    n = len(data)
    unique_values, counts = np.unique(data, return_counts=True)
    probabilities = counts / n

    theoretical_probabilities_dict = {i: (1 - p) ** i * p for i in range(max(unique_values) + 1)}

    aligned_theoretical_probabilities = []
    for val in unique_values:
        aligned_theoretical_probabilities.append(theoretical_probabilities_dict.get(val, 0))

    return unique_values, probabilities, np.array(aligned_theoretical_probabilities)


def main():
    p = float(input("Введите вероятность обнаружения P: "))
    num_trials = int(input("Введите количество экспериментов: "))
    data = simulate_detection(p, num_trials)

    E_eta, D_eta, x, S_squared, med, Rb = calculate_characteristics(p, data)
    unique_values, probabilities, theoretical_probabilities = calculate_probabilities(data, p)

    # Calculate differences
    differences = np.abs(probabilities - np.array(theoretical_probabilities))
    max_difference = np.max(differences)

    # Print results in table format
    print("Теоретические и экспериментальные характеристики")
    print("-----------------------------------")
    print(f"Eη: {E_eta:.4f}  x: {x:.4f} |Eη - x|: {abs(E_eta - x):.4f} ")
    print(f"Dη: {D_eta:.4f}  S²: {S_squared:.4f} |Dη - S²|: {abs(D_eta - S_squared):.4f}")
    print(f"Med: {med:.4f}  Rb: {Rb:.4f}")

    # Print probabilities table
    print("\nТаблица вероятностей")
    print("--------------------")
    print("yj   | P(η=yj) | nj/n | diff")
    for i in range(len(unique_values)):
        print(
            f"{unique_values[i]} | {theoretical_probabilities[i]:.4f} | {probabilities[i]:.4f} | {abs(probabilities[i] - theoretical_probabilities[i]):.4f}")
    print(f"\nМаксимальное отклонение: {max_difference:.4f}")

    # --- Measure Difference ---
    measure_diff = 0.0
    measure_diff = np.max(np.abs(np.array(theoretical_probabilities) - np.array(probabilities)))
    print(f"Мера расхождения: {measure_diff:.4f}")

    data = simulate_detection(p, num_trials)

    # --- Create theoretical_probabilities_dict ---
    theoretical_probabilities_dict = {i: (1 - p) ** i * p for i in range(max(unique_values) + 1)}

    # --- Plotting Section ---
    plt.figure(figsize=(12, 6))

    # Empirical CDF (no change needed here)
    sorted_data = np.sort(data)
    y_empirical = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    plt.step(sorted_data, y_empirical, where='post', label='Выборочная')

    # Corrected Theoretical CDF
    x_theoretical = np.sort(np.unique(data))
    y_theoretical = np.cumsum([theoretical_probabilities_dict.get(i, 0) for i in x_theoretical])

    plt.step(x_theoretical, y_theoretical, where='post', label='Теоретическая')

    plt.xlabel("Количество циклов (η)")
    plt.ylabel("F(x)")
    plt.title("Функции распределдения")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()