import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

from ui_main import MainWindow
from controller import SyncController


def main():
    app = QApplication(sys.argv)

    controller = SyncController()
    window = MainWindow(controller)

    try:
        controller.initialize()
    except Exception as e:
        QMessageBox.critical(
            None,
            "Ошибка инициализации",
            str(e)
        )
        sys.exit(1)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
