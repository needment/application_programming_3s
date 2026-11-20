import csv
from pathlib import Path


class FilePathIterator:
    """
    Итератор по путям к файлам из CSV-аннотации.
    """

    def __init__(self, annotation_path: Path) -> None:
        """
        Инициализирует итератор на основе файла аннотации.

        :param annotation_path: путь к CSV-файлу аннотации
        """
        if not annotation_path.is_file():
            raise FileNotFoundError(
                f"Файл аннотации не найден: {annotation_path}"
            )

        self._paths: list[str] = []
        self._index: int = 0

        with open(annotation_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if "absolute_path" in row and row["absolute_path"]:
                    self._paths.append(row["absolute_path"])

    def __iter__(self) -> "FilePathIterator":
        """
        Возвращает экземпляр итератора.
        """
        return self

    def __next__(self) -> str:
        """
        Возвращает следующий путь к файлу.
        """
        if self._index < len(self._paths):
            path = self._paths[self._index]
            self._index += 1
            return path
        raise StopIteration
