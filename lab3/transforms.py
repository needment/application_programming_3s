import random

import numpy as np


def invert_colors(image: np.ndarray) -> np.ndarray:
    """
    Инвертирует цвета изображения.

    :param image: исходное изображение (uint8)
    :return: изображение с инвертированными цветами
    """
    return (255 - image).astype(np.uint8)


def _get_grid_size(parts: int) -> tuple[int, int]:
    """
    Подбирает количество строк и столбцов для разбиения на заданное
    количество равных частей (максимально близко к квадратной сетке).

    :param parts: общее количество частей
    :return: кортеж (строки, столбцы)
    """
    rows = int(parts**0.5)
    while parts % rows != 0:
        rows -= 1
    cols = parts // rows
    return rows, cols


def make_puzzle(image: np.ndarray, parts: int) -> np.ndarray:
    """
    Делит изображение на заданное количество равных частей и собирает их
    в случайном порядке в изображение того же размера.

    :param image: исходное изображение
    :param parts: количество частей паззла (>= 1)
    :return: перемешанное изображение
    """
    if parts < 1:
        raise ValueError("Количество частей паззла должно быть >= 1")

    height, width = image.shape[:2]
    rows, cols = _get_grid_size(parts)
    tile_h = height // rows
    tile_w = width // cols

    if tile_h == 0 or tile_w == 0:
        raise ValueError("Слишком много частей для данного размера изображения")

    tiles: list[np.ndarray] = []
    for r in range(rows):
        for c in range(cols):
            y1, y2 = r * tile_h, (r + 1) * tile_h
            x1, x2 = c * tile_w, (c + 1) * tile_w
            tiles.append(image[y1:y2, x1:x2].copy())

    random.shuffle(tiles)

    result = image.copy()
    idx = 0
    for r in range(rows):
        for c in range(cols):
            y1, y2 = r * tile_h, (r + 1) * tile_h
            x1, x2 = c * tile_w, (c + 1) * tile_w
            result[y1:y2, x1:x2] = tiles[idx]
            idx += 1

    return result


def add_white_noise(image: np.ndarray, intensity: float) -> np.ndarray:
    """
    Накладывает на изображение белый (гауссовский) шум.

    :param image: исходное изображение
    :param intensity: стандартное отклонение шума (>= 0)
    :return: изображение с шумом
    """
    if intensity < 0:
        raise ValueError("Интенсивность шума не может быть отрицательной")

    noise = np.random.normal(0.0, intensity, image.shape)
    noisy_image = np.clip(image.astype(np.float32) + noise, 0, 255)
    return noisy_image.astype(np.uint8)
