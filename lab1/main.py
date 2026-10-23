"""
Основной модуль: чтение, валидация, сортировка и сохранение анкет.
"""

import argparse
import re
import sys

from validators import KEYS, is_valid_record


def load_records(file_path: str) -> list[dict[str, str]]:
    """
    Чтение и первичный разбор анкет из текстового файла.

    :param file_path: Путь к входному файлу.
    :return: Список словарей с данными анкет.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    if not content:
        return []

    blocks = [b.strip() for b in re.split(r'\n\s*\n', content) if b.strip()]
    records: list[dict[str, str]] = []
    for block in blocks:
        rec: dict[str, str] = {}
        for line in block.splitlines():
            if ':' in line:
                key, val = line.split(':', 1)
                rec[key.strip()] = val.strip()
        if rec:
            records.append(rec)
    return records


def format_records(records: list[dict[str, str]]) -> str:
    """
    Преобразование списка словарей анкет в форматированную строку.

    :param records: Список анкет.
    :return: Результирующий текст.
    """
    formatted_blocks: list[str] = []
    for i, rec in enumerate(records, start=1):
        block_lines = [f"{i})"]
        for key in KEYS:
            block_lines.append(f"{key}: {rec[key]}")
        formatted_blocks.append('\n'.join(block_lines))
    return '\n\n'.join(formatted_blocks)


def save_records(file_path: str, data: str) -> None:
    """
    Запись строковых данных в файл.

    :param file_path: Путь к выходному файлу.
    :param data: Текст для записи.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data + ('\n' if data else ''))


def main() -> None:
    """
    Точка входа в программу: разбор аргументов командной строки,
    вызов валидации, сортировка и вывод результатов.
    """
    parser = argparse.ArgumentParser(
        description='Обработка, валидация и сортировка анкетных данных.'
    )
    parser.add_argument('input_file', type=str, help='Путь к входному файлу с анкетами')
    parser.add_argument(
        '-o', '--output', type=str, default='result.txt', help='Путь к файлу результата'
    )
    args = parser.parse_args()

    try:
        records = load_records(args.input_file)
    except OSError as exc:
        print(f"Ошибка чтения входного файла: {exc}", file=sys.stderr)
        return

    valid_records = [rec for rec in records if is_valid_record(rec)]
    sorted_records = sorted(valid_records, key=lambda x: (x['Фамилия'], x['Имя']))
    formatted_output = format_records(sorted_records)

    try:
        save_records(args.output, formatted_output)
    except OSError as exc:
        print(f"Ошибка записи в выходной файл: {exc}", file=sys.stderr)
        return

    print(formatted_output)


if __name__ == '__main__':
    main()