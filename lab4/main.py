from pathlib import Path

import pandas as pd

from data_processing import (
    add_rgb_brightness_columns,
    filter_by_range,
    load_annotation,
    save_dataframe,
    sort_by_column,
)
from visualization import plot_rgb_histogram_curves

ANNOTATION_CSV = Path("/home/larper/UniCoding/application_programming_3s/lab2/dataset/annotation.csv")
OUTPUT_CSV = Path("output/rgb_brightness_sorted.csv")
OUTPUT_PLOT = Path("output/rgb_brightness_histogram.png")

HAS_CSV_HEADER = True
SORT_COLUMN = "mean_r"
FILTER_COLUMN = "mean_r"
FILTER_MIN = 50.0
FILTER_MAX = 200.0


def main() -> None:
    """
    Основной сценарий выполнения лабораторной работы № 4 (вариант 5).
    """
    try:
        df = load_annotation(ANNOTATION_CSV, has_header=HAS_CSV_HEADER)
        df = add_rgb_brightness_columns(df)

        sorted_df = sort_by_column(df, column=SORT_COLUMN, ascending=True)
        filtered_df = filter_by_range(
            sorted_df,
            column=FILTER_COLUMN,
            min_value=FILTER_MIN,
            max_value=FILTER_MAX,
        )

        print("Отсортированный DataFrame (первые 5 строк):")
        print(sorted_df.head())
        print(
            f"\nОтфильтровано ({FILTER_MIN} <= {FILTER_COLUMN} <= {FILTER_MAX}): "
            f"{len(filtered_df)} из {len(sorted_df)} изображений."
        )

        save_dataframe(sorted_df, OUTPUT_CSV)
        plot_rgb_histogram_curves(sorted_df, OUTPUT_PLOT, bins=30, show=True)

        print(f"\nDataFrame сохранён в: {OUTPUT_CSV}")
        print(f"График сохранён в: {OUTPUT_PLOT}")
    except (
        FileNotFoundError,
        ValueError,
        OSError,
        pd.errors.EmptyDataError,
    ) as exc:
        print(f"Ошибка выполнения: {exc}")


if __name__ == "__main__":
    main()
