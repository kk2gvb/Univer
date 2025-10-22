#!/bin/bash

echo "Анализ надежности системы - Вариант 20"
echo "========================================"

# Проверяем установлен ли Python
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python3 не установлен"
    exit 1
fi

# Проверяем установлены ли библиотеки
echo "Проверка зависимостей..."
python3 -c "import matplotlib, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Установка необходимых библиотек..."
    pip3 install matplotlib numpy --user
fi

# Запускаем анализ
echo "Запуск анализа..."
python3 1.py

echo ""
echo "Анализ завершен! Графики сохранены в папке 'graphs/'"
