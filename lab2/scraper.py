import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36"
    )
}
TIMEOUT = 10


def parse_price(price_text: str) -> float:
    """
    Извлекает числовое значение цены из строки.

    :param price_text: строка с ценой (например, '£51.77')
    :return: цена в виде float
    """
    match = re.search(r"\d+(?:\.\d+)?", price_text)
    if not match:
        raise ValueError(f"Не удалось распознать цену: {price_text}")
    return float(match.group())


def fetch_soup(url: str) -> BeautifulSoup:
    """
    Загружает HTML-страницу и возвращает объект BeautifulSoup.

    :param url: адрес страницы
    :return: разобранный HTML-документ
    """
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def download_image(img_url: str, save_path: Path) -> None:
    """
    Скачивает изображение по URL и сохраняет его на диск.

    :param img_url: ссылка на изображение
    :param save_path: путь для сохранения файла
    """
    response = requests.get(img_url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    save_path.write_bytes(response.content)


def scrape_covers(
    min_price: float,
    output_dir: Path,
    count: int = 30,
) -> list[Path]:
    """
    Скачивает обложки книг с ценой строго выше заданной.

    :param min_price: минимальная цена книги
    :param output_dir: папка для сохранения обложек
    :param count: количество обложек для скачивания
    :return: список путей к скачанным файлам
    """
    if min_price < 0:
        raise ValueError("Минимальная цена не может быть отрицательной.")
    if count <= 0:
        raise ValueError("Количество обложек должно быть больше нуля.")

    output_dir.mkdir(parents=True, exist_ok=True)
    saved_paths: list[Path] = []
    current_url: str | None = BASE_URL

    while current_url and len(saved_paths) < count:
        soup = fetch_soup(current_url)
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            if len(saved_paths) >= count:
                break

            price_tag = book.find("p", class_="price_color")
            img_tag = book.find("img")
            if not price_tag or not img_tag or not img_tag.get("src"):
                continue

            price = parse_price(price_tag.get_text())
            if price <= min_price:
                continue

            img_url = urljoin(current_url, str(img_tag["src"]))
            file_path = output_dir / f"cover_{len(saved_paths) + 1:03d}.jpg"

            try:
                download_image(img_url, file_path)
                saved_paths.append(file_path)
            except requests.RequestException as exc:
                print(f"Ошибка при скачивании {img_url}: {exc}")

        next_li = soup.find("li", class_="next")
        next_link = next_li.find("a") if next_li else None
        if next_link and next_link.get("href"):
            current_url = urljoin(current_url, str(next_link["href"]))
        else:
            current_url = None

    return saved_paths
