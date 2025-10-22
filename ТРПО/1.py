import matplotlib.pyplot as plt
import numpy as np
import os

# Устанавливаем русские шрифты для Linux
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# Создаем папку для графиков если её нет
if not os.path.exists('graphs'):
    os.makedirs('graphs')

# Данные для варианта 20
data = [0.022, 0.028, 0.032, 0.004, 0.207, 0.079, 0.027, 0.015, 0.032, 0.002, 
        0.001, 0.011, 0.016, 0.093, 0.008, 0.148, 0.022, 0.041, 0.216, 0.096]

N0 = 100

print("Строим графики...")

# 1. График вероятности безотказной работы p*(0,t)
plt.figure(figsize=(10, 6))

# Сортируем времена отказа
sorted_times = sorted(data)

# Рассчитываем накопленные отказы и вероятности
times_for_plot = [0] + sorted_times + [sorted_times[-1] + 0.01]
survival_prob = [1.0]

current_failures = 0
for t in sorted_times:
    current_failures += 1
    survival_prob.append((N0 - current_failures) / N0)

survival_prob.append(survival_prob[-1])

plt.step(times_for_plot, survival_prob, where='post', linewidth=2, color='blue')
plt.xlabel('Время, t (усл. ед.)')
plt.ylabel('Вероятность безотказной работы p*(0,t)')
plt.title('Вероятность безотказной работы системы')
plt.grid(True, alpha=0.3)
plt.ylim(0.75, 1.02)
plt.xlim(0, 0.25)
plt.tight_layout()
plt.savefig('graphs/survival_probability.jpg', dpi=300, bbox_inches='tight')
plt.close()
print("✓ График 1 сохранен: graphs/survival_probability.jpg")

# 2. Графики частоты и интенсивности отказов (отдельные)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Параметры интервалов
dt = 0.05
intervals = [(0.00, 0.05), (0.05, 0.10), (0.10, 0.15), (0.15, 0.20), (0.20, 0.25)]
interval_centers = [0.025, 0.075, 0.125, 0.175, 0.225]

# Данные из таблицы 2
failures_count = [13, 4, 1, 1, 1]
Ni_values = [87, 83, 82, 81, 80]
N_avg = [93.5, 85.0, 82.5, 81.5, 80.5]
a_star = [2.600, 0.800, 0.200, 0.200, 0.200]
lambda_star = [2.780, 0.941, 0.242, 0.245, 0.248]

bar_width = 0.015

# График частоты отказов a*(t)
bars1 = ax1.bar(interval_centers, a_star, width=bar_width, alpha=0.7, color='red', label='a*(t) - Частота отказов')
ax1.set_xlabel('Время, t (усл. ед.)')
ax1.set_ylabel('Частота отказов a*(t)')
ax1.set_title('Частота отказов системы')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Добавляем значения над столбцами
for i, v in enumerate(a_star):
    ax1.text(interval_centers[i], v + 0.1, f'{v:.3f}', ha='center', va='bottom')

# График интенсивности отказов λ*(t)
bars2 = ax2.bar(interval_centers, lambda_star, width=bar_width, alpha=0.7, color='green', label='λ*(t) - Интенсивность отказов')
ax2.set_xlabel('Время, t (усл. ед.)')
ax2.set_ylabel('Интенсивность отказов λ*(t)')
ax2.set_title('Интенсивность отказов системы')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Добавляем значения над столбцами
for i, v in enumerate(lambda_star):
    ax2.text(interval_centers[i], v + 0.1, f'{v:.3f}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('graphs/failure_rates_separate.jpg', dpi=300, bbox_inches='tight')
plt.close()
print("✓ График 2 сохранен: graphs/failure_rates_separate.jpg")

# 3. Совмещенный график частоты и интенсивности отказов
plt.figure(figsize=(10, 6))

x_pos_combined = np.array(interval_centers)
bar_width_combined = 0.01

bars_a = plt.bar(x_pos_combined - bar_width_combined/2, a_star, width=bar_width_combined, 
                alpha=0.7, color='red', label='a*(t) - Частота отказов')
bars_lambda = plt.bar(x_pos_combined + bar_width_combined/2, lambda_star, width=bar_width_combined, 
                     alpha=0.7, color='green', label='λ*(t) - Интенсивность отказов')

plt.xlabel('Время, t (усл. ед.)')
plt.ylabel('Значения критериев')
plt.title('Сравнение частоты и интенсивности отказов')
plt.grid(True, alpha=0.3)
plt.legend()

# Добавляем значения над столбцами
for i, (a_val, l_val) in enumerate(zip(a_star, lambda_star)):
    plt.text(x_pos_combined[i] - bar_width_combined/2, a_val + 0.1, f'{a_val:.2f}', 
             ha='center', va='bottom', fontsize=8)
    plt.text(x_pos_combined[i] + bar_width_combined/2, l_val + 0.1, f'{l_val:.2f}', 
             ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('graphs/failure_rates_combined.jpg', dpi=300, bbox_inches='tight')
plt.close()
print("✓ График 3 сохранен: graphs/failure_rates_combined.jpg")

# 4. Гистограмма распределения отказов
plt.figure(figsize=(10, 6))

plt.hist(data, bins=10, alpha=0.7, color='orange', edgecolor='black')
plt.xlabel('Время до отказа (усл. ед.)')
plt.ylabel('Количество отказов')
plt.title('Гистограмма распределения времени до отказа')
plt.grid(True, alpha=0.3)

# Добавляем вертикальную линию для среднего времени
mean_time = sum(data) / len(data)
plt.axvline(mean_time, color='red', linestyle='--', linewidth=2, 
           label=f'Среднее время (T₀ = {mean_time:.3f})')
plt.legend()

plt.tight_layout()
plt.savefig('graphs/failure_distribution.jpg', dpi=300, bbox_inches='tight')
plt.close()
print("✓ График 4 сохранен: graphs/failure_distribution.jpg")

# 5. Дополнительный график: вероятность отказа q*(0,t)
plt.figure(figsize=(10, 6))

failure_prob = [1 - p for p in survival_prob]

plt.step(times_for_plot, failure_prob, where='post', linewidth=2, color='red')
plt.xlabel('Время, t (усл. ед.)')
plt.ylabel('Вероятность отказа q*(0,t)')
plt.title('Вероятность отказа системы')
plt.grid(True, alpha=0.3)
plt.ylim(-0.02, 0.27)
plt.xlim(0, 0.25)
plt.tight_layout()
plt.savefig('graphs/failure_probability.jpg', dpi=300, bbox_inches='tight')
plt.close()
print("✓ График 5 сохранен: graphs/failure_probability.jpg")

# Вывод основных статистических данных
print("\n" + "="*50)
print("ОСНОВНЫЕ СТАТИСТИЧЕСКИЕ ДАННЫЕ:")
print("="*50)
print(f"Общее количество систем: N₀ = {N0}")
print(f"Количество наблюдаемых отказов: {len(data)}")
print(f"Среднее время безотказной работы: T₀ = {mean_time:.3f} усл. ед.")
print(f"Минимальное время до отказа: {min(data):.3f} усл. ед.")
print(f"Максимальное время до отказа: {max(data):.3f} усл. ед.")
print(f"Общее время наблюдения: {sum(data):.3f} усл. ед.")
print(f"Стандартное отклонение: {np.std(data):.3f} усл. ед.")

print("\n" + "="*50)
print("ВСЕ ГРАФИКИ СОХРАНЕНЫ В ПАПКЕ 'graphs/'")
print("Файлы:")
print("  1. survival_probability.jpg - Вероятность безотказной работы")
print("  2. failure_rates_separate.jpg - Частота и интенсивность отказов (отдельно)")
print("  3. failure_rates_combined.jpg - Частота и интенсивность отказов (совмещенно)")
print("  4. failure_distribution.jpg - Распределение отказов")
print("  5. failure_probability.jpg - Вероятность отказа")
print("="*50)
