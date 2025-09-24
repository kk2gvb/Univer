import matplotlib.pyplot as plt

states = ["a0", "a1", "a2"]
state_labels = ["a0 (Закрыто)", "a1 (Открывается)", "a2 (Открыто)"] 

inputs = ["z0", "z1"]

transitions = {
    "a0": {"z0": "a0", "z1": "a1"},
    "a1": {"z0": "a1", "z1": "a2"},
    "a2": {"z0": "a2", "z1": "a0"},
}

outputs = {"a0": "y0 (Закрыто)", "a1": "y1 (Открывается)", "a2": "y2 (Открыто)"}

test_inputs = ["z0", "z1", "z1", "z0", "z1"]

current_state = "a0"  
states_over_time = [current_state]  

print("Проверка автомата Мили на адекватность")
print(f"Начальное состояние: {current_state}")

for signal in test_inputs:
    next_state = transitions[current_state][signal]
    output = outputs[next_state]
    print(f"Вход: {signal} | Состояние: {current_state} | Выход: {output} | Следующее состояние: {next_state}")
    current_state = next_state
    states_over_time.append(current_state)

time = list(range(len(states_over_time)))
state_to_num = {state: i for i, state in enumerate(states)}  # Числовые индексы
numeric_states = [state_to_num[state] for state in states_over_time]

plt.figure(figsize=(10, 6))
plt.step(time, numeric_states, where="post", label="Состояние автомата")
plt.xticks(time)
plt.yticks(range(len(states)), state_labels)
plt.xlabel("Время")
plt.ylabel("Состояние")
plt.title("Изменение состояния автомата Мили по времени")
plt.legend()
plt.grid(True)

plt.savefig("automaton_plot.png")

print("График сохранён как automaton_plot.png. Открой файл, чтобы посмотреть!")
