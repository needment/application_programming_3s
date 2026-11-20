"""Главное окно приложения для просмотра датасета изображений (вариант 5)."""

import sys
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from lab2.iterator import FilePathIterator

WINDOW_TITLE: str = "Просмотр датасета изображений"
WINDOW_WIDTH: int = 800
WINDOW_HEIGHT: int = 600
IMAGE_MIN_WIDTH: int = 400
IMAGE_MIN_HEIGHT: int = 300


class MainWindow(QMainWindow):
    """Главное окно приложения для просмотра изображений из датасета."""

    def __init__(self) -> None:
        """Инициализация главного окна и состояния приложения."""
        super().__init__()
        self._iterator: FilePathIterator | None = None
        self._current_pixmap: QPixmap | None = None

        self._init_ui()

    def _init_ui(self) -> None:
        """Создание и компоновка элементов графического интерфейса."""
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.annotation_button = QPushButton("Выбрать аннотацию (.csv)", self)
        self.annotation_button.clicked.connect(self.select_annotation)

        self.image_label = QLabel("Выберите CSV-файл аннотации", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(IMAGE_MIN_WIDTH, IMAGE_MIN_HEIGHT)
        self.image_label.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Ignored
        )
        self.image_label.setStyleSheet("border: 1px solid #cccccc;")

        self.next_button = QPushButton("Следующее изображение", self)
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.show_next_image)

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.annotation_button)
        main_layout.addWidget(self.image_label, stretch=1)
        main_layout.addWidget(self.next_button)

        self.statusBar().showMessage("Файл аннотации не выбран")

    def select_annotation(self) -> None:
        """Открывает диалог выбора CSV-файла аннотации."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл аннотации", "", "CSV файлы (*.csv)"
        )
        if file_path:
            self._load_dataset(Path(file_path))

    def _load_dataset(self, annotation_path: Path) -> None:
        """
        Инициализирует итератор датасета и отображает первое изображение.

        :param annotation_path: путь к CSV-файлу аннотации.
        """
        try:
            self._iterator = FilePathIterator(annotation_path)
        except (FileNotFoundError, OSError, UnicodeDecodeError) as exc:
            QMessageBox.critical(self, "Ошибка загрузки", str(exc))
            return

        self._current_pixmap = None
        self.next_button.setEnabled(True)
        self.show_next_image()

    def show_next_image(self) -> None:
        """Получает следующий путь из итератора и отображает изображение."""
        if self._iterator is None:
            return

        try:
            image_path = next(self._iterator)
        except StopIteration:
            QMessageBox.information(
                self,
                "Конец датасета",
                "Изображения в файле аннотации закончились.",
            )
            self.next_button.setEnabled(False)
            self.statusBar().showMessage("Просмотр датасета завершён")
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            QMessageBox.warning(
                self,
                "Ошибка чтения файла",
                f"Не удалось загрузить изображение:\n{image_path}",
            )
            return

        self._current_pixmap = pixmap
        self._update_pixmap_display()
        self.statusBar().showMessage(f"Файл: {Path(image_path).name}")

    def _update_pixmap_display(self) -> None:
        """
        Отображает текущее изображение в исходном размере или уменьшенным
        с сохранением пропорций (без растягивания больше оригинала).
        """
        if self._current_pixmap is None:
            return

        target_size = self.image_label.size()
        orig_w = self._current_pixmap.width()
        orig_h = self._current_pixmap.height()

        if orig_w > target_size.width() or orig_h > target_size.height():
            scaled_pixmap = self._current_pixmap.scaled(
                target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setPixmap(self._current_pixmap)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Пересчитывает размер отображаемого изображения при изменении окна.

        :param event: событие изменения размера окна.
        """
        super().resizeEvent(event)
        self._update_pixmap_display()


def main() -> None:
    """Точка входа в приложение."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
