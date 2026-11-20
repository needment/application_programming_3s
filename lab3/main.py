import argparse

from io_utils import load_image, save_image, show_comparison
from transforms import add_white_noise, invert_colors, make_puzzle


def parse_args() -> argparse.Namespace:
    """
    Считывает аргументы командной строки.

    :return: объект с переданными параметрами
    """
    parser = argparse.ArgumentParser(
        description="Лабораторная работа №3, вариант 5: "
                    "инверсия, паззл, белый шум."
    )
    parser.add_argument(
        "input_path",
        type=str,
        help="Путь к исходному изображению",
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="Путь для сохранения результата",
    )
    parser.add_argument(
        "-p",
        "--parts",
        type=int,
        default=9,
        help="Количество частей паззла (по умолчанию: 9)",
    )
    parser.add_argument(
        "-n",
        "--noise",
        type=float,
        default=25.0,
        help="Интенсивность белого шума (по умолчанию: 25.0)",
    )
    return parser.parse_args()


def main() -> None:
    """
    Основная функция программы.
    """
    try:
        args = parse_args()

        image = load_image(args.input_path)
        height, width, channels = image.shape
        print(
            f"Размер изображения: {width}x{height}, каналов: {channels} "
            f"(shape={image.shape})"
        )

        result = invert_colors(image)
        result = make_puzzle(result, args.parts)
        result = add_white_noise(result, args.noise)

        save_image(args.output_path, result)
        print(f"Результат сохранён в: {args.output_path}")

        show_comparison(image, result)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Ошибка: {exc}")


if __name__ == "__main__":
    main()
