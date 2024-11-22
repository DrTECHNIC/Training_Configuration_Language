import pytest, tempfile, os
from main import *


# Тестирование функции parse_custom_config
def test_parse_custom_config_valid():
    test_input = '''set name = @"Даниил" // Объявление имени пользователя
                    set age = 18 // Объявление возраста пользователя
                    set copy_name = ?[name] // Копирование имени
                    set features = { @"1", @"feature2", ?[copy_name], 19 }'''

    # Создаем временный файл для тестирования
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        f.write(test_input)
        temp_file = f.name

    # Парсим файл
    config_data = parse_custom_config(temp_file)
    os.remove(temp_file)  # Удаляем временный файл после теста

    assert config_data is not None
    assert len(config_data) == 4  # Ожидаем 4 строки данных

    # Проверяем правильность парсинга
    assert config_data[0] == ('name', 'Даниил', 'Объявление имени пользователя')
    assert config_data[1] == ('age', 18, 'Объявление возраста пользователя')
    assert config_data[2] == ('copy_name', 'Даниил', 'Копирование имени')
    assert config_data[3] == ('features', ['1', 'feature2', 'Даниил', 19], None)


def test_parse_custom_config_invalid_syntax():
    test_input = '''set name = @"Даниил" // Объявление имени пользователя
                    set age = "invalid_value"'''  # Некорректное значение для "age"

    # Создаем временный файл для тестирования
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        f.write(test_input)
        temp_file = f.name

    # Парсим файл
    config_data = parse_custom_config(temp_file)
    os.remove(temp_file)  # Удаляем временный файл после теста

    # Проверяем, что возникла ошибка и возвращается None
    assert config_data is None


def test_parse_custom_config_unknown_constant():
    test_input = '''set name = @"Даниил"
                    set copy_name = ?[Unknown_name]'''

    # Создаем временный файл для тестирования
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        f.write(test_input)
        temp_file = f.name

    # Парсим файл
    config_data = parse_custom_config(temp_file)
    os.remove(temp_file)  # Удаляем временный файл после теста

    # Проверяем, что возникла ошибка на неизвестную константу
    assert config_data is None


# Тестирование функции generate_toml
def test_generate_toml():
    config_data = [
        ("name", "Даниил", "Объявление имени пользователя"),
        ("age", 18, None),
        ("copy_name", "Даниил", None),
        ("features", ["feature1", "feature2", "Даниил", 42], None)
    ]

    expected_output = '''name = "Даниил" # Объявление имени пользователя
age = 18
copy_name = "Даниил"
features = ["feature1", "feature2", "Даниил", 42]'''

    toml_output = generate_toml(config_data)

    assert toml_output.strip() == expected_output.strip()


# Тестирование обработки пустого файла
def test_parse_empty_file():
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        temp_file = f.name

    # Парсим пустой файл
    config_data = parse_custom_config(temp_file)
    os.remove(temp_file)  # Удаляем временный файл после теста

    assert config_data == []


# Тестирование обработки комментирования
def test_comment_handling():
    test_input = '''set name = @"John" // Это имя
                    set age = 25 // Это возраст'''

    # Создаем временный файл для тестирования
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        f.write(test_input)
        temp_file = f.name

    # Парсим файл
    config_data = parse_custom_config(temp_file)
    os.remove(temp_file)  # Удаляем временный файл после теста

    assert config_data[0][2] == "Это имя"
    assert config_data[1][2] == "Это возраст"


# Тест на генерацию TOML с комментариями
def test_generate_toml_with_comments():
    config_data = [
        ("name", "John", "Это имя"),
        ("age", 25, "Это возраст")
    ]

    expected_output = '''name = "John" # Это имя
age = 25 # Это возраст'''

    toml_output = generate_toml(config_data)

    assert toml_output.strip() == expected_output.strip()


if __name__ == "__main__":
    pytest.main()
