import cv2
import matplotlib.pyplot as plt
import numpy as np


def load_image(path: str) -> np.ndarray:
    """
    Загружает изображение из файла.

    :param path: путь к исходному файлу
    :return: массив пикселей изображения (BGR)
    """
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Не удалось открыть изображение: {path}")
    return image


def save_image(path: str, image: np.ndarray) -> None:
    """
    Сохраняет изображение в файл.

    :param path: путь для сохранения
    :param image: массив пикселей изображения
    """
    if not cv2.imwrite(path, image):
        raise OSError(f"Не удалось сохранить изображение: {path}")


def show_comparison(original: np.ndarray, result: np.ndarray) -> None:
    """
    Отображает исходное и преобразованное изображения с помощью Matplotlib.

    :param original: исходное изображение (BGR)
    :param result: итоговое изображение (BGR)
    """
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(original_rgb)
    axes[0].set_title("Исходное изображение")
    axes[0].axis("off")

    axes[1].imshow(result_rgb)
    axes[1].set_title("Результат (инверсия + паззл + шум)")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()
