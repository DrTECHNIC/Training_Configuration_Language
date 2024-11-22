import argparse, re


def parse_custom_config(input_file):
    config_data = []
    constants = {}

    def parse_value(value):
        # Удаление кавычек и обработка значений
        if value.startswith('@"') and value.endswith('"'):
            return value[2:-1]  # Убираем @" и "
        elif value.isdigit():
            return int(value)
        elif re.match(r"^[0-9]*\.[0-9]+$", value):
            return float(value)
        elif value.startswith("{") and value.endswith("}"):
            return [parse_value(v.strip()) for v in split_array(value[1:-1])]
        elif value.startswith("?[") and value.endswith("]"):
            reference_key = value[2:-1]
            if reference_key in constants:
                return constants[reference_key]
            else:
                raise ValueError(f"Неизвестная константа: {reference_key}")
        else:
            # Обработка случаев с недопустимыми значениями
            if not value.isdigit() and not re.match(r"^[0-9]*\.[0-9]+$", value):
                raise ValueError(f"Неверное значение: {value}")
            return value

    def split_array(array_string):
        result = []
        buffer = ""
        depth = 0

        for char in array_string:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
            if char == ',' and depth == 0:
                result.append(buffer.strip())
                buffer = ""
            else:
                buffer += char
        if buffer.strip():
            result.append(buffer.strip())
        return result

    def extract_comment(line):
        if "//" in line:
            return line.split("//", 1)
        return line, None

    try:
        with open(input_file, 'r', encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                if line.startswith("//"):
                    config_data.append((None, None, line[2:]))
                    continue

                line, comment = extract_comment(line)
                line = line.strip()
                comment = comment.strip() if comment else None

                if line.startswith("set"):
                    match = re.match(r"set\s+([_a-zA-Z][_a-zA-Z0-9]*)\s*=\s*(.+)", line)
                    if match:
                        key, value = match.groups()
                        try:
                            parsed_value = parse_value(value)
                        except ValueError as e:
                            print(f"Ошибка синтаксиса в строке {line_number}: {e}")
                            return None  # Возвращаем None в случае ошибки
                        constants[key] = parsed_value
                        config_data.append((key, parsed_value, comment))
                    else:
                        print(f"Ошибка синтаксиса в строке {line_number}.")
                        return None  # Возвращаем None в случае ошибки
                elif line:
                    print(f"Ошибка синтаксиса в строке {line_number}.")
                    return None  # Возвращаем None для незнакомых конструкций
    except Exception as e:
        print(f"Ошибка при чтении файла '{input_file}': {e}")
        return None

    return config_data


def generate_toml(config_data):
    lines = []

    def format_value(value):
        if isinstance(value, str):
            return f'"{value}"'  # Форматируем строку в кавычках
        elif isinstance(value, list):
            return "[" + ", ".join(format_value(item) for item in value) + "]"
        else:
            return str(value)

    for key, value, comment in config_data:
        if key and value:
            line = f"{key} = {format_value(value)}"
            if comment:
                line += f" # {comment}"
        elif comment:
            line = f"#{comment}"
        lines.append(line)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Преобразование учебного конфигурационного языка в TOML.")
    parser.add_argument("input_file", help="Путь к входному файлу конфигурации")

    args = parser.parse_args()

    config_data = parse_custom_config(args.input_file)
    if config_data is None:
        return

    toml_output = generate_toml(config_data)
    print(toml_output)


if __name__ == "__main__":
    main()
