from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, UnidentifiedImageError

PATH_COLUMNS = ("absolute_path", "relative_path")
RGB_COLUMNS = ("mean_r", "mean_g", "mean_b")


def load_annotation(
    csv_path: str | Path,
    has_header: bool = True,
) -> pd.DataFrame:
    """
    Загружает CSV-аннотацию и формирует DataFrame с путями к файлам.

    :param csv_path: путь к CSV-файлу из лабораторной работы № 2
    :param has_header: содержит ли CSV строку заголовков
    :return: DataFrame с колонками absolute_path и relative_path
    """
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"Файл аннотации не найден: {path}")

    header = 0 if has_header else None
    df = pd.read_csv(path, header=header)

    if df.shape[1] < 2:
        raise ValueError("CSV-файл должен содержать минимум 2 колонки.")

    result = df.iloc[:, :2].copy()
    result.columns = list(PATH_COLUMNS)
    return result


def calculate_rgb_means(image_path: str | Path) -> tuple[float, float, float]:
    """
    Вычисляет среднюю яркость изображения по каналам R, G и B.

    :param image_path: путь к файлу изображения
    :return: кортеж средних значений (mean_r, mean_g, mean_b)
    """
    with Image.open(image_path) as img:
        rgb_array = np.asarray(img.convert("RGB"), dtype=np.float64)

    mean_r, mean_g, mean_b = rgb_array.mean(axis=(0, 1))
    return float(mean_r), float(mean_g), float(mean_b)


def add_rgb_brightness_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет в DataFrame колонки со средней яркостью по каналам R, G и B.

    :param df: исходный DataFrame с путями к изображениям
    :return: новый DataFrame с добавленными колонками mean_r, mean_g, mean_b
    """
    result = df.copy()
    rgb_values: list[tuple[float, float, float]] = []

    for abs_path, rel_path in zip(
        result["absolute_path"],
        result["relative_path"],
    ):
        img_path = Path(str(abs_path))
        if not img_path.is_file():
            img_path = Path(str(rel_path))

        try:
            rgb_values.append(calculate_rgb_means(img_path))
        except (FileNotFoundError, UnidentifiedImageError, OSError) as exc:
            print(f"Предупреждение: не удалось обработать '{img_path}': {exc}")
            rgb_values.append((np.nan, np.nan, np.nan))

    rgb_df = pd.DataFrame(rgb_values, columns=list(RGB_COLUMNS), index=result.index)
    return pd.concat([result, rgb_df], axis=1)


def sort_by_column(
    df: pd.DataFrame,
    column: str,
    ascending: bool = True,
) -> pd.DataFrame:
    """
    Сортирует DataFrame по указанной колонке.

    :param df: исходный DataFrame
    :param column: название колонки для сортировки
    :param ascending: сортировка по возрастанию, если True
    :return: отсортированный DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Колонка '{column}' отсутствует в DataFrame.")

    return df.sort_values(
        by=column,
        ascending=ascending,
        ignore_index=True,
    )


def filter_by_range(
    df: pd.DataFrame,
    column: str,
    min_value: float = 0.0,
    max_value: float = 255.0,
) -> pd.DataFrame:
    """
    Фильтрует строки DataFrame по диапазону значений указанной колонки.

    :param df: исходный DataFrame
    :param column: название колонки для фильтрации
    :param min_value: нижняя граница диапазона (включительно)
    :param max_value: верхняя граница диапазона (включительно)
    :return: отфильтрованный DataFrame
    """
    if column not in df.columns:
        raise ValueError(f"Колонка '{column}' отсутствует в DataFrame.")
    if min_value > max_value:
        raise ValueError("min_value не может быть больше max_value.")

    mask = df[column].between(min_value, max_value)
    return df.loc[mask].reset_index(drop=True)


def save_dataframe(df: pd.DataFrame, output_path: str | Path) -> None:
    """
    Сохраняет DataFrame в CSV-файл.

    :param df: DataFrame для сохранения
    :param output_path: путь для сохранения файла
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
