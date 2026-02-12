# experimental_learning_test.py
"""
ПРОСТОЙ ФАЙЛ ДЛЯ ОБУЧЕНИЯ САМОПЕРЕПИСЫВАНИЯ
Намеренно содержит ошибки для исправления
"""

# 1. Дублирование кода (система должна убрать)
def calc_sum1(nums):
    total = 0
    for n in nums:
        total += n
    return total

def calc_sum2(numbers):  # Точно такая же функция!
    total = 0
    for num in numbers:
        total += num
    return total

# 2. Слишком длинная функция
def very_long_function():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
    v = 22
    w = 23
    x = 24
    y = 25
    z = 26
    aa = 27
    return "слишком длинно"

# 3. Вложенные циклы
def nested_loops():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for l in range(10):  # 4 уровня вложенности!
                    print(f"{i}-{j}-{k}-{l}")

# 4. Мало комментариев
def uncommented():
    x = [1,2,3,4,5]
    y = []
    for i in x:
        y.append(i*2)
    return y