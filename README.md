# **Задание №3**
Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из входного формата в выходной. Синтаксические ошибки выявляются с выдачей сообщений.

Входной текст на **учебном конфигурационном языке** принимается из файла, путь к которому задан ключом командной строки. Выходной текст на **языке toml** попадает в стандартный вывод.

Однострочные комментарии:

```// Это однострочный комментарий```

Массивы:

```{ значение, значение, значение, ... }```

Имена:

```[_a-zA-Z][_a-zA-Z0-9]*```

Значения:
- ```Числа.```
- ```Строки.```
- ```Массивы.```

Строки:

```@"Это строка"```

Объявление константы на этапе трансляции:

```set имя = значение```

Вычисление константы на этапе трансляции:

```?[имя]```

Результатом вычисления константного выражения является значение.

Все конструкции учебного конфигурационного языка (с учетом их возможной вложенности) должны быть покрыты тестами. Необходимо показать 3 примера описания конфигураций из разных предметных областей.

# Установка
Перед началом работы с программой требуется скачать репозиторий и необходимые библиотеки.

Клонирование репозитория:
```Bash
git clone https://github.com/DrTECHNIC/Training_Configuration_Language
```
Скачивание библиотеки [pytest](https://github.com/pytest-dev/pytest) путём запуска файла [script.sh](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/script.sh):
```Bash
script.sh
```
# Запуск
Запуск [main.py](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/main.py):
```Bash
py main.py <имя_файла>
```
Запуск [test.py](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/test.py):
```Bash
pytest -v test.py
```
# Тесты
## Тест 1
### Входные данные
![](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/test1_input.png)
### Выходные данные
![](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/test1_output.png)
## Тест 2
### Входные данные
![](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/test2_input.png)
### Выходные данные
![](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/test2_output.png)
## Тест 3
### Входные данные
![](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/test3_input.png)
### Выходные данные
![](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/test3_output.png)
## Общие тесты
![](https://github.com/DrTECHNIC/Training_Configuration_Language/blob/main/pytest.png)
