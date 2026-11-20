import csv
import os
from pathlib import Path


def create_annotation(file_paths: list[Path], csv_path: Path) -> None:
    """
    Создаёт CSV-файл аннотации с абсолютным и относительным путями к файлам.

    :param file_paths: список путей к скачанным файлам
    :param csv_path: путь к итоговому CSV-файлу
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["absolute_path", "relative_path"])

        for path in file_paths:
            abs_path = str(path.resolve())
            rel_path = os.path.relpath(path)
            writer.writerow([abs_path, rel_path])
