"""
Модуль валидации анкетных данных с использованием регулярных выражений.
"""

from datetime import date
import re

RE_NAME = re.compile(r'^[A-ZА-ЯЁ][a-zа-яёA-ZА-ЯЁ\-]*$')
RE_GENDER = re.compile(r'^(?:[МмЖж]|[Мм]ужской|[Жж]енский)$')
RE_DATE = re.compile(r'^(\d{1,2})([./-])(\d{1,2})\2(\d{4})$')
RE_PHONE = re.compile(
    r'^(?:\+7|8)(?:\d{10}|(?:\s?\(\d{3}\)|\s\d{3})\s?\d{3}[-\s]\d{2}[-\s]\d{2})$'
)
RE_EMAIL = re.compile(r'^[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$')
RE_CITY = re.compile(r'^(?:г\.\s*)?[A-ZА-ЯЁ][a-zа-яёA-ZА-ЯЁ\s\-]*$')

KEYS: list[str] = [
    'Фамилия',
    'Имя',
    'Пол',
    'Дата рождения',
    'Номер телефона или email',
    'Город',
]


def is_valid_date(value: str) -> bool:
    """
    Проверка формата и календарной корректности даты.

    :param value: Строка с датой.
    :return: True, если дата существует и входит в диапазон от 1900 года до текущего, иначе False.
    """
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
    """
    Проверка соответствия всех полей анкеты правилам.

    :param rec: Словарь с полями анкеты.
    :return: True, если все обязательные поля присутствуют и валидны, иначе False.
    """
    if not all(k in rec for k in KEYS):
        return False
    return (
        bool(RE_NAME.fullmatch(rec['Фамилия']))
        and bool(RE_NAME.fullmatch(rec['Имя']))
        and bool(RE_GENDER.fullmatch(rec['Пол']))
        and is_valid_date(rec['Дата рождения'])
        and (
            bool(RE_PHONE.fullmatch(rec['Номер телефона или email']))
            or bool(RE_EMAIL.fullmatch(rec['Номер телефона или email']))
        )
        and bool(RE_CITY.fullmatch(rec['Город']))
    )