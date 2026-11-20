import argparse
from pathlib import Path

import requests

from annotation import create_annotation
from iterator import FilePathIterator
from scraper import scrape_covers


def parse_args() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки.

    :return: объект с переданными аргументами
    """
    parser = argparse.ArgumentParser(
        description="Скачивание обложек книг дороже заданной цены."
    )
    parser.add_argument(
        "--min-price",
        type=float,
        required=True,
        help="Минимальная цена книги (скачиваются книги строго дороже).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Путь к папке для сохранения обложек.",
    )
    parser.add_argument(
        "--annotation",
        type=Path,
        required=True,
        help="Путь к CSV-файлу аннотации.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=30,
        help="Количество обложек для скачивания (по умолчанию: 30).",
    )
    return parser.parse_args()


def main() -> None:
    """
    Основная функция программы.
    """
    args = parse_args()

    try:
        saved_files = scrape_covers(
            min_price=args.min_price,
            output_dir=args.output_dir,
            count=args.count,
        )
        create_annotation(saved_files, args.annotation)
        print(f"Скачано обложек: {len(saved_files)}")
        print(f"Аннотация сохранена в: {args.annotation}")

        print("\nПроверка итератора:")
        iterator = FilePathIterator(args.annotation)
        for file_path in iterator:
            print(file_path)

    except (ValueError, OSError, requests.RequestException) as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
