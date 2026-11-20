from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CHANNELS = (
    ("mean_r", "red", "Канал R"),
    ("mean_g", "green", "Канал G"),
    ("mean_b", "blue", "Канал B"),
)


def plot_rgb_histogram_curves(
    df: pd.DataFrame,
    output_path: str | Path,
    bins: int = 30,
    show: bool = True,
) -> None:
    """
    Строит гистограмму в виде 3 кривых (R, G, B), сохраняет и отображает график.

    :param df: отсортированный DataFrame с колонками mean_r, mean_g, mean_b
    :param output_path: путь для сохранения графика
    :param bins: количество интервалов гистограммы
    :param show: отображать ли график на экране
    """
    required_columns = [col for col, _, _ in CHANNELS]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Отсутствуют колонки для графика: {missing}")

    if bins <= 0:
        raise ValueError("Количество интервалов (bins) должно быть > 0.")

    valid_df = df[required_columns].dropna()
    if valid_df.empty:
        raise ValueError("Нет корректных данных для построения графика.")

    plt.figure(figsize=(10, 6))

    for column, color, label in CHANNELS:
        counts, bin_edges = np.histogram(
            valid_df[column],
            bins=bins,
            range=(0.0, 255.0),
        )
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        plt.plot(bin_centers, counts, color=color, linewidth=2, label=label)

    plt.title("Гистограмма средней яркости изображений по каналам R, G, B")
    plt.xlabel("Средняя яркость (0–255)")
    plt.ylabel("Количество изображений")
    plt.xlim(0, 255)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    plt.close()
