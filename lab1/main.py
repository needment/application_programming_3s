import argparse
import re
from datetime import date

RE_NAME = re.compile(r'^[A-ZА-ЯЁ][a-zа-яёA-ZА-ЯЁ\-]*$')
RE_GENDER = re.compile(r'^(?:[МмЖж]|[Мм]ужской|[Жж]енский)$')
RE_DATE = re.compile(r'^(\d{1,2})([./-])(\d{1,2})\2(\d{4})$')
RE_PHONE = re.compile(r'^(?:\+7|8)(?:\d{10}|(?:\s?\(\d{3}\)|\s\d{3})\s?\d{3}[-\s]\d{2}[-\s]\d{2})$')
RE_EMAIL = re.compile(r'^[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$')
RE_CITY = re.compile(r'^(?:г\.\s*)?[A-ZА-ЯЁ][a-zа-яёA-ZА-ЯЁ\s\-]*$')

KEYS = [
    'Фамилия',
    'Имя',
    'Пол',
    'Дата рождения',
    'Номер телефона или email',
    'Город',
]


def is_valid_date(value: str) -> bool:
    match = RE_DATE.fullmatch(value)
    if not match:
        return False
    d, _, m, y = match.groups()
    try:
        day, month, year = int(d), int(m), int(y)
        if not (1900 <= year <= date.today().year):
            return False
        date(year, month, day)
        return True
    except ValueError:
        return False


def is_valid_record(rec: dict[str, str]) -> bool:
    if not all(k in rec for k in KEYS):
        return False
    return (
        bool(RE_NAME.fullmatch(rec['Фамилия']))
        and bool(RE_NAME.fullmatch(rec['Имя']))
        and bool(RE_GENDER.fullmatch(rec['Пол']))
        and is_valid_date(rec['Дата рождения'])
        and (bool(RE_PHONE.fullmatch(rec['Номер телефона или email'])) or bool(RE_EMAIL.fullmatch(rec['Номер телефона или email'])))
        and bool(RE_CITY.fullmatch(rec['Город']))
    )


def load_records(file_path: str) -> list[dict[str, str]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    if not content:
        return []

    blocks = [b.strip() for b in re.split(r'\n\s*\n', content) if b.strip()]
    records = []
    for block in blocks:
        rec = {}
        for line in block.splitlines():
            if ':' in line:
                key, val = line.split(':', 1)
                rec[key.strip()] = val.strip()
        if rec:
            records.append(rec)
    return records

# Отсортируйте исходный список по фамилиям и именам в алфавитном порядке
# и сохраните результат в новый файл (структура списка не меняется).

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str)
    parser.add_argument('-o', '--output', type=str, default='result.txt')
    args = parser.parse_args()

    records = load_records(args.input_file)
    valid_records = [rec for rec in records if is_valid_record(rec)]

    sorted_records = sorted(valid_records, key=lambda x: (x['Фамилия'], x['Имя']))

    formatted_blocks = []
    for i, rec in enumerate(sorted_records, start=1):
        block_lines = [f"{i})"]
        for key in KEYS:
            block_lines.append(f"{key}: {rec[key]}")
        formatted_blocks.append('\n'.join(block_lines))

    formatted_output = '\n\n'.join(formatted_blocks)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(formatted_output + ('\n' if formatted_output else ''))

    print(formatted_output)


if __name__ == '__main__':
    main()